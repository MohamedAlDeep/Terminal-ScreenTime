#!/usr/bin/env python3
"""
Linux Screen Time Tracker
Tracks active applications and user activity on Linux systems
Supports both X11 and Wayland (limited) display servers
"""

import os
import time
import csv
import subprocess
import psutil
from datetime import datetime
import json
import logging

# Configuration
LOG_FILE = os.path.join(os.path.expanduser('~'), '.local', 'share', 'screentime', 'activity_log.csv')
LOG_INTERVAL = 60  # Seconds between logs
IDLE_THRESHOLD = 300  # 5 minutes (seconds)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_display_server():
    """Detect the display server (X11, Wayland, etc.)"""
    if os.environ.get('WAYLAND_DISPLAY'):
        return 'wayland'
    elif os.environ.get('DISPLAY'):
        return 'x11'
    else:
        return 'unknown'

def get_idle_time():
    """Get idle time in seconds (X11 only, returns 0 for Wayland)"""
    display_server = get_display_server()
    
    if display_server == 'x11':
        try:
            # Try using xprintidle
            result = subprocess.run(['xprintidle'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return int(result.stdout.strip()) // 1000  # Convert milliseconds to seconds
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Fallback to xssstate
                result = subprocess.run(['xssstate', '-i'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return int(result.stdout.strip())
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                pass
    
    # For Wayland or if X11 tools fail, return 0 (assume active)
    return 0

def is_screensaver_active():
    """Check if screensaver is active"""
    display_server = get_display_server()
    
    if display_server == 'x11':
        try:
            # Check if screen is locked using various methods
            lock_commands = [
                ['xssstate', '-s'],
                ['gnome-screensaver-command', '-q'],
                ['xscreensaver-command', '-version']
            ]
            
            for cmd in lock_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    if 'locked' in result.stdout.lower() or 'active' in result.stdout.lower():
                        return True
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    continue
        except Exception:
            pass
    
    return False

def get_foreground_app_x11():
    """Get foreground application info for X11"""
    try:
        # Get the active window ID
        result = subprocess.run(['xprop', '-root', '_NET_ACTIVE_WINDOW'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return "Unknown", "Unknown"
        
        window_id = result.stdout.strip().split()[-1]
        if window_id == '0x0':
            return "Desktop", "Desktop"
        
        # Get window title
        title_result = subprocess.run(['xprop', '-id', window_id, 'WM_NAME'], 
                                    capture_output=True, text=True, timeout=5)
        title = "Unknown"
        if title_result.returncode == 0 and '=' in title_result.stdout:
            title = title_result.stdout.split('=', 1)[1].strip().strip('"')
        
        # Get process info
        pid_result = subprocess.run(['xprop', '-id', window_id, '_NET_WM_PID'], 
                                  capture_output=True, text=True, timeout=5)
        app_name = "Unknown"
        if pid_result.returncode == 0 and '=' in pid_result.stdout:
            try:
                pid = int(pid_result.stdout.split('=')[1].strip())
                process = psutil.Process(pid)
                app_name = process.name()
            except (ValueError, psutil.NoSuchProcess):
                pass
        
        return app_name, title
        
    except Exception as e:
        logger.warning(f"Error getting X11 window info: {e}")
        return "Unknown", "Unknown"

def get_foreground_app_wayland():
    """Get foreground application info for Wayland (limited)"""
    try:
        # Try to get info from various Wayland compositors
        methods = [
            # GNOME/Mutter
            ['gdbus', 'call', '--session', '--dest', 'org.gnome.Shell',
             '--object-path', '/org/gnome/Shell', '--method', 'org.gnome.Shell.Eval',
             'global.display.focus_window.get_wm_class()'],
            
            # KDE/KWin
            ['qdbus', 'org.kde.KWin', '/KWin', 'org.kde.KWin.activeWindow'],
            
            # Sway
            ['swaymsg', '-t', 'get_tree']
        ]
        
        for method in methods:
            try:
                result = subprocess.run(method, capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    if 'swaymsg' in method:
                        # Parse Sway JSON output
                        data = json.loads(result.stdout)
                        focused = find_focused_window(data)
                        if focused:
                            return focused.get('app_id', 'Unknown'), focused.get('name', 'Unknown')
                    else:
                        # Basic parsing for other methods
                        output = result.stdout.strip()
                        if output and output != 'null':
                            return output, output
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
                continue
        
        # Fallback: try to get the most active process
        return get_active_process_fallback()
        
    except Exception as e:
        logger.warning(f"Error getting Wayland window info: {e}")
        return "Unknown", "Unknown"

def find_focused_window(node):
    """Recursively find the focused window in Sway tree"""
    if isinstance(node, dict):
        if node.get('focused'):
            return node
        for child in node.get('nodes', []) + node.get('floating_nodes', []):
            result = find_focused_window(child)
            if result:
                return result
    return None

def get_active_process_fallback():
    """Fallback method to guess the active application"""
    try:
        # Get processes sorted by CPU usage
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                proc_info = proc.info
                if proc_info['cpu_percent'] > 0:
                    processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage and return the most active GUI application
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        # Filter for likely GUI applications
        gui_apps = ['firefox', 'chrome', 'chromium', 'code', 'gedit', 'nautilus', 
                   'terminal', 'konsole', 'gnome-terminal', 'kate', 'libreoffice']
        
        for proc in processes:
            for gui_app in gui_apps:
                if gui_app in proc['name'].lower():
                    return proc['name'], proc['name']
        
        # If no GUI app found, return the most active process
        if processes:
            return processes[0]['name'], processes[0]['name']
        
    except Exception as e:
        logger.warning(f"Error in fallback method: {e}")
    
    return "Unknown", "Unknown"

def get_foreground_app():
    """Get foreground application info based on display server"""
    display_server = get_display_server()
    
    if display_server == 'x11':
        return get_foreground_app_x11()
    elif display_server == 'wayland':
        return get_foreground_app_wayland()
    else:
        return get_active_process_fallback()

def setup_logging():
    """Setup CSV logging"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'idle_seconds', 'app_name', 'window_title'])

def log_activity():
    """Main logging loop"""
    setup_logging()
    display_server = get_display_server()
    
    print(f"Starting Linux Screen Time Tracker")
    print(f"Display Server: {display_server}")
    print(f"Logging to: {LOG_FILE}")
    print("Press Ctrl+C to stop tracking...")
    
    if display_server == 'wayland':
        print("Note: Wayland support is limited. Some features may not work.")
    
    try:
        while True:
            idle_time = get_idle_time()
            screensaver = is_screensaver_active()
            active = idle_time < IDLE_THRESHOLD and not screensaver
            
            if active:
                app_name, window_title = get_foreground_app()
            else:
                app_name, window_title = "Idle", "System Idle"
            
            timestamp = datetime.now().isoformat()
            
            # Clean the window title to avoid encoding issues
            try:
                window_title = str(window_title).encode('ascii', 'ignore').decode('ascii')
                if not window_title.strip():
                    window_title = "Unknown Window"
            except:
                window_title = "Unknown Window"
            
            with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, idle_time, app_name, window_title])
            
            # Optional: print current activity (remove in production)
            if active:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {app_name} - {window_title}")
            
            time.sleep(LOG_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nTracker stopped.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nError: {e}")

if __name__ == "__main__":
    log_activity()
