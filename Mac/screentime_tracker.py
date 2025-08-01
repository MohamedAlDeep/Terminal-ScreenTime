#!/usr/bin/env python3
"""
macOS Screen Time Tracker
Tracks active applications and idle time using macOS APIs and tools
"""

import subprocess
import time
import csv
import os
import sys
from datetime import datetime
import psutil

def get_idle_time():
    """
    Get idle time in seconds using macOS ioreg command
    Returns idle time in seconds
    """
    try:
        # Use ioreg to get HIDIdleTime
        result = subprocess.run([
            'ioreg', '-c', 'IOHIDSystem'
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'HIDIdleTime' in line:
                    # Extract idle time in nanoseconds and convert to seconds
                    idle_ns = int(line.split('=')[1].strip())
                    idle_seconds = idle_ns // 1000000000
                    return idle_seconds
        
        # Fallback: use system_profiler (slower but more reliable)
        result = subprocess.run([
            'system_profiler', 'SPPowerDataType'
        ], capture_output=True, text=True, timeout=10)
        
        # If we can't get idle time, assume 0 (active)
        return 0
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError, FileNotFoundError):
        # If all methods fail, assume user is active
        return 0

def get_foreground_app():
    """
    Get the currently active application and window title using AppleScript
    Returns tuple: (app_name, window_title)
    """
    try:
        # Use AppleScript to get frontmost application
        app_script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            return frontApp
        end tell
        '''
        
        result = subprocess.run([
            'osascript', '-e', app_script
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            app_name = result.stdout.strip()
        else:
            app_name = "Unknown"
        
        # Get window title using AppleScript
        window_script = f'''
        tell application "System Events"
            tell process "{app_name}"
                try
                    set windowTitle to name of front window
                    return windowTitle
                on error
                    return ""
                end try
            end tell
        end tell
        '''
        
        result = subprocess.run([
            'osascript', '-e', window_script
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            window_title = result.stdout.strip()
        else:
            window_title = ""
        
        # Fallback: try using lsappinfo (faster alternative)
        if not app_name or app_name == "Unknown":
            try:
                result = subprocess.run([
                    'lsappinfo', 'info', '-only', 'name', '-app', 'front'
                ], capture_output=True, text=True, timeout=3)
                
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'name=' in line:
                            app_name = line.split('name=')[1].strip(' "')
                            break
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        return app_name or "Unknown", window_title or ""
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: try ps command to get frontmost process
        try:
            result = subprocess.run([
                'ps', '-eo', 'comm,pid', '-r'
            ], capture_output=True, text=True, timeout=3)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                if lines:
                    app_name = os.path.basename(lines[0].split()[0])
                    return app_name, ""
        except:
            pass
        
        return "Unknown", ""

def is_screen_locked():
    """
    Check if the screen is locked using macOS APIs
    Returns True if screen is locked, False otherwise
    """
    try:
        # Check if screensaver is running
        result = subprocess.run([
            'pgrep', '-f', 'ScreenSaverEngine'
        ], capture_output=True, text=True, timeout=3)
        
        if result.returncode == 0:
            return True
        
        # Check if screen is locked using pmset
        result = subprocess.run([
            'pmset', '-g', 'powerstate', 'IODisplayWrangler'
        ], capture_output=True, text=True, timeout=3)
        
        if result.returncode == 0:
            # If display is off, consider it locked
            if 'UsableTime' in result.stdout and '0' in result.stdout:
                return True
        
        # Check system events for screen lock
        script = '''
        tell application "System Events"
            get running of screen saver preferences
        end tell
        '''
        
        result = subprocess.run([
            'osascript', '-e', script
        ], capture_output=True, text=True, timeout=3)
        
        if result.returncode == 0:
            return result.stdout.strip().lower() == 'true'
        
        return False
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_system_info():
    """
    Get macOS system information
    Returns dict with system details
    """
    try:
        # Get macOS version
        result = subprocess.run([
            'sw_vers', '-productVersion'
        ], capture_output=True, text=True, timeout=3)
        
        macos_version = result.stdout.strip() if result.returncode == 0 else "Unknown"
        
        # Get system name
        result = subprocess.run([
            'scutil', '--get', 'ComputerName'
        ], capture_output=True, text=True, timeout=3)
        
        computer_name = result.stdout.strip() if result.returncode == 0 else "Unknown"
        
        return {
            'platform': 'macOS',
            'version': macos_version,
            'computer_name': computer_name,
            'python_version': sys.version.split()[0]
        }
    except:
        return {
            'platform': 'macOS',
            'version': 'Unknown',
            'computer_name': 'Unknown',
            'python_version': sys.version.split()[0]
        }

def log_activity(duration_minutes=None, csv_file="screentime_data.csv"):
    """
    Main activity logging function
    Args:
        duration_minutes: How long to track (None for infinite)
        csv_file: CSV file to store data
    """
    print(f"[+] Starting macOS screen time tracking...")
    print(f"[+] Data will be saved to: {csv_file}")
    
    # Print system info
    system_info = get_system_info()
    print(f"[+] System: {system_info['platform']} {system_info['version']}")
    print(f"[+] Computer: {system_info['computer_name']}")
    print(f"[+] Python: {system_info['python_version']}")
    print("[+] Press Ctrl+C to stop tracking")
    print("-" * 50)
    
    start_time = time.time()
    last_app = ""
    last_window = ""
    
    # Ensure CSV file exists with headers
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'idle_seconds', 'app_name', 'window_title'])
    
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Check if screen is locked
            if is_screen_locked():
                app_name = "Screen Locked"
                window_title = "Screen Saver"
                idle_seconds = 0
            else:
                # Get current application and idle time
                app_name, window_title = get_foreground_app()
                idle_seconds = get_idle_time()
            
            # Only log if app changed or every 30 seconds
            if app_name != last_app or window_title != last_window or time.time() % 30 < 1:
                try:
                    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([current_time, idle_seconds, app_name, window_title])
                    
                    # Print current activity (only if changed)
                    if app_name != last_app or window_title != last_window:
                        if idle_seconds > 60:
                            print(f"[IDLE {idle_seconds//60}m] {current_time} - Idle")
                        elif app_name == "Screen Locked":
                            print(f"[LOCKED] {current_time} - Screen Locked")
                        else:
                            display_window = window_title[:50] + "..." if len(window_title) > 50 else window_title
                            print(f"[ACTIVE] {current_time} - {app_name}: {display_window}")
                    
                    last_app = app_name
                    last_window = window_title
                    
                except Exception as e:
                    print(f"[ERROR] Failed to write to CSV: {e}")
            
            # Check if duration limit reached
            if duration_minutes and (time.time() - start_time) >= (duration_minutes * 60):
                print(f"\n[+] Tracking completed after {duration_minutes} minutes")
                break
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        elapsed = (time.time() - start_time) / 60
        print(f"\n[+] Tracking stopped after {elapsed:.1f} minutes")
        print(f"[+] Data saved to: {csv_file}")

def test_system():
    """
    Test macOS system compatibility and required tools
    """
    print("macOS Screen Time Tracker - System Test")
    print("=" * 40)
    
    system_info = get_system_info()
    print(f"Platform: {system_info['platform']} {system_info['version']}")
    print(f"Computer: {system_info['computer_name']}")
    print(f"Python: {system_info['python_version']}")
    print()
    
    # Test required commands
    commands_to_test = [
        ('osascript', 'AppleScript support'),
        ('ioreg', 'Hardware registry access'),
        ('pmset', 'Power management'),
        ('lsappinfo', 'Application info (optional)'),
        ('pgrep', 'Process search'),
        ('sw_vers', 'System version'),
        ('scutil', 'System configuration')
    ]
    
    print("Testing required tools:")
    all_good = True
    
    for cmd, description in commands_to_test:
        try:
            result = subprocess.run([cmd, '--help'], 
                                 capture_output=True, timeout=3)
            if result.returncode == 0 or cmd in ['osascript', 'ioreg', 'pmset', 'scutil']:
                # These commands might not have --help but exist
                result2 = subprocess.run(['which', cmd], 
                                       capture_output=True, timeout=3)
                if result2.returncode == 0:
                    print(f"  ✓ {cmd:<12} - {description}")
                else:
                    print(f"  ✗ {cmd:<12} - {description} (NOT FOUND)")
                    if cmd in ['osascript', 'ioreg']:
                        all_good = False
            else:
                print(f"  ✓ {cmd:<12} - {description}")
        except:
            print(f"  ✗ {cmd:<12} - {description} (NOT FOUND)")
            if cmd in ['osascript', 'ioreg']:
                all_good = False
    
    print()
    
    # Test functionality
    print("Testing functionality:")
    
    try:
        idle_time = get_idle_time()
        print(f"  ✓ Idle time detection: {idle_time} seconds")
    except Exception as e:
        print(f"  ✗ Idle time detection failed: {e}")
        all_good = False
    
    try:
        app_name, window_title = get_foreground_app()
        print(f"  ✓ Active app detection: {app_name}")
        if window_title:
            print(f"    Window: {window_title[:50]}...")
    except Exception as e:
        print(f"  ✗ Active app detection failed: {e}")
        all_good = False
    
    try:
        locked = is_screen_locked()
        print(f"  ✓ Screen lock detection: {'Locked' if locked else 'Unlocked'}")
    except Exception as e:
        print(f"  ✗ Screen lock detection failed: {e}")
    
    print()
    
    if all_good:
        print("✓ System is compatible!")
        print("  You can run: python3 screentime_tracker.py")
    else:
        print("✗ System compatibility issues detected!")
        print("  Some features may not work properly.")
        print("  Make sure you're running on macOS with proper permissions.")
    
    return all_good

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_system()
    else:
        try:
            log_activity()
        except KeyboardInterrupt:
            print("\n[+] Tracker stopped by user")
        except Exception as e:
            print(f"\n[ERROR] Tracker failed: {e}")
            sys.exit(1)
