import os
import time
import csv
import win32gui
import win32api
import win32con
import win32process
import psutil
from datetime import datetime
from ctypes import Structure, windll, c_uint, sizeof, byref

# Configuration
LOG_FILE = os.path.join(os.getenv('LOCALAPPDATA'), 'ScreenTime', 'activity_log.csv')
LOG_INTERVAL = 60  # Seconds between logs
IDLE_THRESHOLD = 300  # 5 minutes (seconds)

class LASTINPUTINFO(Structure):
    _fields_ = [("cbSize", c_uint),
                ("dwTime", c_uint)]

def get_idle_time():
    info = LASTINPUTINFO()
    info.cbSize = sizeof(LASTINPUTINFO)
    windll.user32.GetLastInputInfo(byref(info))
    return (windll.kernel32.GetTickCount() - info.dwTime) // 1000

def is_screensaver_active():
    try:
        # Try to use win32gui to check screensaver status
        return win32gui.SystemParametersInfo(win32con.SPI_GETSCREENSAVERRUNNING, 0, None, 0)
    except:
        # If that fails, assume screensaver is not active
        return False

def get_foreground_app():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process = psutil.Process(pid)
        exe = process.exe()
        name = os.path.basename(exe)
    except:
        name = "Unknown"
    return name, title

def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'idle_seconds', 'app_name', 'window_title'])

def log_activity():
    setup_logging()
    print(f"📊 Starting Screen Time Tracker. Logging to: {LOG_FILE}")
    print("Press Ctrl+C to stop tracking...")
    
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
                window_title = window_title.encode('ascii', 'ignore').decode('ascii')
            except:
                window_title = "Unknown Window"
            
            with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, idle_time, app_name, window_title])
            
            time.sleep(LOG_INTERVAL)
    except KeyboardInterrupt:
        print("\nTracker stopped.")

if __name__ == "__main__":
    log_activity()