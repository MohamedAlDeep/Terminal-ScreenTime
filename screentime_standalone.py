"""
Screen Time Tracker - Complete Standalone Executable
This file contains all functionality needed for the executable to work independently
"""
import os
import sys
import subprocess
import argparse
import threading
import time
import csv
from datetime import datetime, timedelta
import signal
import json

# Windows-specific imports
if sys.platform == 'win32':
    try:
        import win32gui
        import win32process
        import psutil
        import ctypes
        from ctypes import wintypes
        WINDOWS_APIS_AVAILABLE = True
    except ImportError:
        WINDOWS_APIS_AVAILABLE = False
        print("Warning: Windows APIs not available. Some features may not work.")

# Try to import pandas, but provide fallback functionality
try:
    import pandas as pd
    import numpy as np  # pandas dependency
    PANDAS_AVAILABLE = True
    print("[DEBUG] Pandas successfully imported")
except ImportError as e:
    # For PyInstaller builds, pandas should be available
    if hasattr(sys, 'frozen'):
        print(f"[WARNING] Pandas should be available in frozen executable but failed: {e}")
        # Try to force import
        try:
            import pandas as pd
            PANDAS_AVAILABLE = True
            print("[DEBUG] Pandas force import successful")
        except:
            PANDAS_AVAILABLE = False
            print("[DEBUG] Pandas force import failed, using fallback")
    else:
        PANDAS_AVAILABLE = False
        print(f"[DEBUG] Pandas not available: {e}")

# Global constants
LOG_FILE = "screentime_data.csv"
LOCK_FILE = "screentime.lock"

class ScreenTimeTracker:
    """Standalone screen time tracker with all functionality built-in"""
    
    def __init__(self):
        self.running = False
        self.log_file = LOG_FILE
    
    def get_idle_time(self):
        """Get system idle time in seconds"""
        if not WINDOWS_APIS_AVAILABLE:
            return 0
        
        try:
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [('cbSize', wintypes.UINT), ('dwTime', wintypes.DWORD)]
            
            lastInputInfo = LASTINPUTINFO()
            lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
            millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
            return millis / 1000.0
        except:
            return 0
    
    def get_foreground_app(self):
        """Get currently active application"""
        if not WINDOWS_APIS_AVAILABLE:
            return "Unknown", "Unknown"
        
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                window_title = win32gui.GetWindowText(hwnd)
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                
                try:
                    process = psutil.Process(pid)
                    app_name = process.name()
                except:
                    app_name = "Unknown"
                
                return app_name, window_title
        except:
            pass
        
        return "Unknown", "Unknown"
    
    def is_screen_locked(self):
        """Check if screen is locked"""
        if not WINDOWS_APIS_AVAILABLE:
            return False
        
        try:
            import ctypes
            hUser32 = ctypes.windll.user32
            return hUser32.OpenDesktopW("Default", 0, False, 0x0100) == 0
        except:
            return False
    
    def log_activity(self, duration_minutes=None):
        """Main activity logging function"""
        print("[+] Starting screen time tracking...")
        print(f"[+] Data will be saved to: {self.log_file}")
        print("[+] Press Ctrl+C to stop tracking")
        print("-" * 40)
        
        # Create lock file
        try:
            with open(LOCK_FILE, 'w') as f:
                f.write(str(os.getpid()))
        except:
            pass
        
        # Ensure CSV file exists with headers
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['timestamp', 'idle_seconds', 'app_name', 'window_title'])
        
        self.running = True
        start_time = time.time()
        last_app = ""
        last_window = ""
        
        try:
            while self.running:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Check if screen is locked
                if self.is_screen_locked():
                    app_name = "Screen Locked"
                    window_title = "Screen Saver"
                    idle_seconds = 0
                else:
                    # Get current application and idle time
                    app_name, window_title = self.get_foreground_app()
                    idle_seconds = int(self.get_idle_time())
                
                # Only log if app changed or every 30 seconds
                if app_name != last_app or window_title != last_window or time.time() % 30 < 1:
                    try:
                        with open(self.log_file, 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow([current_time, idle_seconds, app_name, window_title])
                        
                        # Print current activity (only if changed)
                        if app_name != last_app or window_title != last_window:
                            if idle_seconds > 60:
                                print(f"[IDLE {idle_seconds//60}m] {current_time} - User idle")
                            elif app_name == "Screen Locked":
                                print(f"[LOCKED] {current_time} - Screen locked")
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
            print("\n[+] Tracking stopped by user")
        finally:
            self.running = False
            # Remove lock file
            try:
                os.remove(LOCK_FILE)
            except:
                pass

class ScreenTimeCLI:
    """Command-line interface for screen time analysis"""
    
    def __init__(self):
        self.log_file = LOG_FILE
    
    def load_data_simple(self):
        """Load data without pandas"""
        if not os.path.exists(self.log_file):
            return []
        
        data = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['timestamp'] = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                    row['idle_seconds'] = int(row['idle_seconds'])
                    data.append(row)
        except Exception as e:
            print(f"Error loading data: {e}")
        
        return data
    
    def load_data_pandas(self):
        """Load data with pandas"""
        if not os.path.exists(self.log_file):
            return None
        
        try:
            encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(self.log_file, encoding=encoding)
                    if not df.empty:
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        return df
                except (UnicodeDecodeError, pd.errors.EmptyDataError):
                    continue
        except Exception as e:
            print(f"Error loading data: {e}")
        
        return None
    
    def format_time(self, minutes):
        """Format minutes into hours and minutes"""
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"
    
    def today_summary(self):
        """Generate today's summary"""
        if PANDAS_AVAILABLE:
            return self._today_summary_pandas()
        else:
            return self._today_summary_simple()
    
    def _today_summary_pandas(self):
        """Today's summary using pandas"""
        df = self.load_data_pandas()
        if df is None or df.empty:
            print(f"\n[i] No activity recorded for today ({datetime.now().date()})")
            return
        
        today = datetime.now().date()
        today_data = df[df['timestamp'].dt.date == today]
        
        if today_data.empty:
            print(f"\n[i] No activity recorded for today ({today})")
            return
        
        # Calculate statistics
        active_data = today_data[today_data['idle_seconds'] < 300]  # Less than 5 minutes idle
        active_minutes = len(active_data)
        unique_apps = active_data['app_name'].nunique() if not active_data.empty else 0
        
        print(f"\nTODAY'S SUMMARY ({today})")
        print("=" * 40)
        print(f"Active Time: {self.format_time(active_minutes)}")
        print(f"Apps Used: {unique_apps}")
        
        # Top apps
        if not active_data.empty:
            top_apps = active_data['app_name'].value_counts().head(5)
            print(f"\nMost Used Apps:")
            for app, count in top_apps.items():
                print(f"  - {app}: {count} minutes")
    
    def _today_summary_simple(self):
        """Today's summary without pandas"""
        data = self.load_data_simple()
        if not data:
            print(f"\n[i] No activity recorded for today ({datetime.now().date()})")
            return
        
        today = datetime.now().date()
        today_data = [row for row in data if row['timestamp'].date() == today]
        
        if not today_data:
            print(f"\n[i] No activity recorded for today ({today})")
            return
        
        # Calculate statistics
        active_data = [row for row in today_data if row['idle_seconds'] < 300]
        active_minutes = len(active_data)
        unique_apps = len(set(row['app_name'] for row in active_data))
        
        print(f"\nTODAY'S SUMMARY ({today})")
        print("=" * 40)
        print(f"Active Time: {self.format_time(active_minutes)}")
        print(f"Apps Used: {unique_apps}")
        
        # Top apps
        if active_data:
            app_counts = {}
            for row in active_data:
                app = row['app_name']
                app_counts[app] = app_counts.get(app, 0) + 1
            
            sorted_apps = sorted(app_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"\nMost Used Apps:")
            for app, count in sorted_apps:
                print(f"  - {app}: {count} minutes")
    
    def check_status(self):
        """Check if tracking is running"""
        # Check lock file and validate process
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE, 'r') as f:
                    pid = int(f.read().strip())
                
                # Check if process is still running
                try:
                    if sys.platform == 'win32':
                        result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], 
                                              capture_output=True, text=True, shell=True)
                        if result.returncode == 0 and str(pid) in result.stdout:
                            print("[+] Tracking is ACTIVE")
                            return True
                    else:
                        # Check if PID exists on Unix
                        os.kill(pid, 0)  # This will raise OSError if process doesn't exist
                        print("[+] Tracking is ACTIVE")
                        return True
                except (subprocess.CalledProcessError, OSError, ProcessLookupError):
                    # Process doesn't exist, remove stale lock file
                    try:
                        os.remove(LOCK_FILE)
                    except:
                        pass
            except (ValueError, FileNotFoundError):
                # Invalid lock file, remove it
                try:
                    os.remove(LOCK_FILE)
                except:
                    pass
        
        print("[-] Tracking is NOT ACTIVE")
        return False
    
    def start_tracking(self):
        """Start tracking in background"""
        if self.check_status():
            print("[+] Tracking is already running!")
            return
        
        # Start tracker in a new process
        try:
            if hasattr(sys, 'frozen'):
                # When running as exe
                current_exe = sys.executable
                subprocess.Popen([current_exe, '--track'], 
                               creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                               cwd=os.path.dirname(current_exe))
            else:
                # When running as script
                subprocess.Popen([sys.executable, __file__, '--track'], 
                               creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            
            print("\n[+] Tracker started in background!")
            print("    It will automatically log your activity.")
            
            # Give it a moment to start
            time.sleep(2)
            
            # Verify it started
            if self.check_status():
                print("    Verification: Tracker is now running ✓")
            else:
                print("    Warning: Could not verify tracker startup")
                
        except Exception as e:
            print(f"[ERROR] Failed to start tracker: {e}")
    
    def stop_tracking(self):
        """Stop background tracking"""
        stopped = False
        
        # Try to remove lock file and kill process
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE, 'r') as f:
                    pid = int(f.read().strip())
                
                if sys.platform == 'win32':
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                                 capture_output=True)
                    stopped = True
                
                os.remove(LOCK_FILE)
            except:
                pass
        
        # Kill any screentime processes
        try:
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/IM', 'ScreenTimeTracker.exe'], 
                             capture_output=True)
                stopped = True
        except:
            pass
        
        if stopped:
            print("[+] Tracking stopped")
        else:
            print("[-] No tracking process found to stop")
    
    def weekly_summary(self):
        """Generate weekly summary using pandas"""
        df = self.load_data_pandas()
        if df is None or df.empty:
            print("\n[i] No activity recorded this week")
            return
        
        # Get the last 7 days
        today = datetime.now().date()
        week_start = today - timedelta(days=6)
        
        week_data = df[df['timestamp'].dt.date >= week_start]
        
        if week_data.empty:
            print(f"\n[i] No activity recorded for the past 7 days")
            return
        
        print(f"\nWEEKLY SUMMARY ({week_start} to {today})")
        print("=" * 50)
        
        # Total time per day
        daily_stats = week_data.groupby(week_data['timestamp'].dt.date).size()
        total_time = daily_stats.sum()
        avg_time = total_time / 7
        
        print(f"Total Active Time: {self.format_time(total_time)}")
        print(f"Daily Average: {self.format_time(int(avg_time))}")
        
        print(f"\nDaily Breakdown:")
        for date, minutes in daily_stats.items():
            day_name = date.strftime('%A')
            print(f"  {day_name} ({date}): {self.format_time(minutes)}")
        
        # Top apps for the week
        app_stats = week_data.groupby('app_name').size().sort_values(ascending=False)
        print(f"\nTop Apps This Week:")
        for app, minutes in app_stats.head(10).items():
            print(f"  - {app}: {self.format_time(minutes)}")
    
    def app_statistics(self):
        """Generate detailed app statistics using pandas"""
        df = self.load_data_pandas()
        if df is None or df.empty:
            print("\n[i] No activity data available")
            return
        
        print(f"\nAPP USAGE STATISTICS")
        print("=" * 40)
        
        # Overall app statistics
        app_stats = df.groupby('app_name').agg({
            'timestamp': ['count', 'min', 'max']
        }).round(2)
        
        app_stats.columns = ['Total_Minutes', 'First_Used', 'Last_Used']
        app_stats = app_stats.sort_values('Total_Minutes', ascending=False)
        
        print(f"Total Apps Tracked: {len(app_stats)}")
        print(f"Total Active Time: {self.format_time(app_stats['Total_Minutes'].sum())}")
        
        print(f"\nTop 15 Applications:")
        print("-" * 60)
        print(f"{'Rank':<4} {'Application':<30} {'Time':<10} {'% of Total':<10}")
        print("-" * 60)
        
        total_minutes = app_stats['Total_Minutes'].sum()
        for i, (app, row) in enumerate(app_stats.head(15).iterrows(), 1):
            percentage = (row['Total_Minutes'] / total_minutes) * 100
            print(f"{i:<4} {app[:28]:<30} {self.format_time(int(row['Total_Minutes'])):<10} {percentage:.1f}%")
        
        # Usage by day of week
        print(f"\nUsage by Day of Week:")
        print("-" * 30)
        df['day_of_week'] = df['timestamp'].dt.day_name()
        daily_usage = df.groupby('day_of_week')['timestamp'].count()
        
        # Order by weekday
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days_order:
            if day in daily_usage:
                minutes = daily_usage[day]
                print(f"  {day}: {self.format_time(minutes)}")
        
        # Usage by hour
        print(f"\nMost Active Hours:")
        print("-" * 20)
        df['hour'] = df['timestamp'].dt.hour
        hourly_usage = df.groupby('hour')['timestamp'].count().sort_values(ascending=False)
        
        for hour, minutes in hourly_usage.head(5).items():
            time_str = f"{hour:02d}:00-{hour+1:02d}:00"
            print(f"  {time_str}: {self.format_time(minutes)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Screen Time Tracker - Standalone')
    parser.add_argument('--track', action='store_true', help='Start background tracking')
    parser.add_argument('--cli', action='store_true', help='Open CLI interface')
    parser.add_argument('--start', action='store_true', help='Start tracking in background')
    parser.add_argument('--stop', action='store_true', help='Stop tracking')
    parser.add_argument('--status', action='store_true', help='Check tracking status')
    parser.add_argument('--today', action='store_true', help='Show today\'s summary')
    parser.add_argument('--week', action='store_true', help='Show weekly report')
    parser.add_argument('--apps', action='store_true', help='Show app usage statistics')
    
    args = parser.parse_args()
    
    # Create instances
    tracker = ScreenTimeTracker()
    cli = ScreenTimeCLI()
    
    # Handle arguments
    if len(sys.argv) == 1:
        print("Screen Time Tracker - Standalone Executable")
        print("=" * 50)
        print("Usage options:")
        print("  --track      Start foreground tracking")
        print("  --start      Start background tracking")
        print("  --stop       Stop tracking")
        print("  --status     Check status")
        print("  --today      Today's summary")
        print("  --week       Weekly report")
        print("  --apps       App usage stats")
        print("\nUse --start to begin tracking in background")
        return
    
    if args.track:
        # Start tracking in foreground
        tracker.log_activity()
    elif args.start:
        cli.start_tracking()
    elif args.stop:
        cli.stop_tracking()
    elif args.status:
        cli.check_status()
    elif args.today:
        cli.today_summary()
    elif args.week:
        if PANDAS_AVAILABLE:
            cli.weekly_summary()
        else:
            print("Weekly reports require pandas. Use --today for basic summary.")
            cli.today_summary()
    elif args.apps:
        if PANDAS_AVAILABLE:
            cli.app_statistics()
        else:
            print("App statistics require pandas. Use --today for basic summary.")
            cli.today_summary()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
