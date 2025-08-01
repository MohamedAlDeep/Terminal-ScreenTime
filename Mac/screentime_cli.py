#!/usr/bin/env python3
"""
macOS Screen Time Tracker - CLI Interface
Command-line interface for tracking management and statistics
"""

import os
import sys
import subprocess
import argparse
import time
import threading
from datetime import datetime, timedelta
import signal

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Install with: pip3 install pandas")
    sys.exit(1)

def load_data(csv_file="screentime_data.csv"):
    """
    Load screen time data with multiple encoding fallbacks
    """
    if not os.path.exists(csv_file):
        print(f"No data file found: {csv_file}")
        return pd.DataFrame()
    
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_file, encoding=encoding)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df
        except (UnicodeDecodeError, pd.errors.EmptyDataError):
            continue
        except Exception as e:
            print(f"Error loading data with {encoding}: {e}")
            continue
    
    print(f"Failed to load data from {csv_file}")
    return pd.DataFrame()

def get_today_summary(csv_file="screentime_data.csv"):
    """
    Generate today's activity summary
    """
    df = load_data(csv_file)
    if df.empty:
        return "No data available for today."
    
    today = datetime.now().date()
    today_data = df[df['timestamp'].dt.date == today].copy()
    
    if today_data.empty:
        return "No activity recorded for today."
    
    # Calculate total time and app usage
    total_entries = len(today_data)
    total_minutes = total_entries * 5 / 60  # Assuming 5-second intervals
    
    # Filter out idle time and screen lock
    active_data = today_data[
        (today_data['idle_seconds'] < 300) & 
        (today_data['app_name'] != 'Screen Locked') &
        (today_data['app_name'] != 'Unknown')
    ].copy()
    
    if active_data.empty:
        return "No active time recorded for today."
    
    # Calculate app usage
    app_usage = active_data['app_name'].value_counts()
    app_time = (app_usage * 5 / 60).round(1)  # Convert to minutes
    
    # Get productive vs unproductive time
    productive_apps = [
        'Xcode', 'Terminal', 'TextEdit', 'VSCode', 'Visual Studio Code',
        'Sublime Text', 'Atom', 'PyCharm', 'IntelliJ IDEA', 'Eclipse',
        'Finder', 'System Preferences', 'Calculator', 'Pages', 'Numbers',
        'Keynote', 'Microsoft Word', 'Microsoft Excel', 'Microsoft PowerPoint',
        'Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma'
    ]
    
    productive_time = 0
    entertainment_time = 0
    
    for app, minutes in app_time.items():
        if any(prod_app.lower() in app.lower() for prod_app in productive_apps):
            productive_time += minutes
        elif any(ent in app.lower() for ent in ['youtube', 'netflix', 'game', 'steam', 'spotify', 'music']):
            entertainment_time += minutes
    
    # Format summary
    summary = []
    summary.append(f"macOS Screen Time Summary - {today.strftime('%B %d, %Y')}")
    summary.append("=" * 50)
    summary.append(f"Total tracking time: {total_minutes:.1f} minutes")
    summary.append(f"Active time: {len(active_data) * 5 / 60:.1f} minutes")
    summary.append(f"Productive time: {productive_time:.1f} minutes")
    summary.append(f"Entertainment time: {entertainment_time:.1f} minutes")
    summary.append("")
    summary.append("Top Applications:")
    summary.append("-" * 30)
    
    for i, (app, minutes) in enumerate(app_time.head(10).items(), 1):
        percentage = (minutes / total_minutes * 100) if total_minutes > 0 else 0
        summary.append(f"{i:2d}. {app:<25} {minutes:6.1f}m ({percentage:4.1f}%)")
    
    return "\n".join(summary)

def get_weekly_summary(csv_file="screentime_data.csv"):
    """
    Generate weekly activity summary
    """
    df = load_data(csv_file)
    if df.empty:
        return "No data available for weekly summary."
    
    # Get last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    week_data = df[
        (df['timestamp'].dt.date >= start_date) & 
        (df['timestamp'].dt.date <= end_date)
    ].copy()
    
    if week_data.empty:
        return "No activity recorded for the past week."
    
    # Daily breakdown
    daily_stats = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        day_data = week_data[week_data['timestamp'].dt.date == day]
        
        if not day_data.empty:
            active_entries = len(day_data[
                (day_data['idle_seconds'] < 300) & 
                (day_data['app_name'] != 'Screen Locked')
            ])
            active_minutes = active_entries * 5 / 60
        else:
            active_minutes = 0
        
        daily_stats.append((day.strftime('%a %m/%d'), active_minutes))
    
    # Weekly totals
    total_active = sum(stat[1] for stat in daily_stats)
    avg_daily = total_active / 7
    
    # App usage for the week
    active_week_data = week_data[
        (week_data['idle_seconds'] < 300) & 
        (week_data['app_name'] != 'Screen Locked') &
        (week_data['app_name'] != 'Unknown')
    ]
    
    if not active_week_data.empty:
        app_usage = active_week_data['app_name'].value_counts()
        app_time = (app_usage * 5 / 60).round(1)
    else:
        app_time = pd.Series()
    
    # Format weekly summary
    summary = []
    summary.append(f"Weekly Screen Time Summary ({start_date} to {end_date})")
    summary.append("=" * 55)
    summary.append(f"Total active time: {total_active:.1f} minutes ({total_active/60:.1f} hours)")
    summary.append(f"Daily average: {avg_daily:.1f} minutes")
    summary.append("")
    summary.append("Daily Breakdown:")
    summary.append("-" * 25)
    
    for day_name, minutes in daily_stats:
        hours = minutes / 60
        bar_length = int(minutes / 20) if minutes > 0 else 0
        bar = "█" * bar_length
        summary.append(f"{day_name}: {minutes:5.1f}m ({hours:4.1f}h) {bar}")
    
    if not app_time.empty:
        summary.append("")
        summary.append("Top Weekly Apps:")
        summary.append("-" * 30)
        
        for i, (app, minutes) in enumerate(app_time.head(10).items(), 1):
            percentage = (minutes / total_active * 100) if total_active > 0 else 0
            summary.append(f"{i:2d}. {app:<25} {minutes:6.1f}m ({percentage:4.1f}%)")
    
    return "\n".join(summary)

def get_app_statistics(csv_file="screentime_data.csv"):
    """
    Generate detailed application usage statistics
    """
    df = load_data(csv_file)
    if df.empty:
        return "No data available for app statistics."
    
    # Filter active data
    active_data = df[
        (df['idle_seconds'] < 300) & 
        (df['app_name'] != 'Screen Locked') &
        (df['app_name'] != 'Unknown')
    ].copy()
    
    if active_data.empty:
        return "No active app data available."
    
    # Calculate app statistics
    app_usage = active_data['app_name'].value_counts()
    app_time = (app_usage * 5 / 60).round(1)  # Convert to minutes
    
    # Categorize apps
    categories = {
        'Development': ['Xcode', 'Terminal', 'VSCode', 'Visual Studio Code', 'Sublime Text', 
                       'Atom', 'PyCharm', 'IntelliJ IDEA', 'Eclipse', 'Git'],
        'Office/Productivity': ['Pages', 'Numbers', 'Keynote', 'Microsoft Word', 
                               'Microsoft Excel', 'Microsoft PowerPoint', 'TextEdit'],
        'Design': ['Adobe Photoshop', 'Adobe Illustrator', 'Sketch', 'Figma', 'Canva'],
        'Web Browsing': ['Safari', 'Chrome', 'Firefox', 'Edge', 'Opera'],
        'Communication': ['Mail', 'Messages', 'Slack', 'Discord', 'Zoom', 'Teams'],
        'Entertainment': ['YouTube', 'Netflix', 'Spotify', 'Music', 'VLC', 'QuickTime'],
        'System': ['Finder', 'System Preferences', 'Activity Monitor', 'Console']
    }
    
    categorized_time = {cat: 0 for cat in categories}
    uncategorized_time = 0
    
    for app, minutes in app_time.items():
        categorized = False
        for category, keywords in categories.items():
            if any(keyword.lower() in app.lower() for keyword in keywords):
                categorized_time[category] += minutes
                categorized = True
                break
        if not categorized:
            uncategorized_time += minutes
    
    # Calculate productivity score
    productive_categories = ['Development', 'Office/Productivity', 'Design']
    productive_time = sum(categorized_time[cat] for cat in productive_categories)
    total_time = sum(app_time)
    productivity_score = (productive_time / total_time * 100) if total_time > 0 else 0
    
    # Format statistics
    summary = []
    summary.append("macOS Application Usage Statistics")
    summary.append("=" * 40)
    summary.append(f"Total apps used: {len(app_time)}")
    summary.append(f"Total active time: {total_time:.1f} minutes ({total_time/60:.1f} hours)")
    summary.append(f"Productivity score: {productivity_score:.1f}%")
    summary.append("")
    
    summary.append("Time by Category:")
    summary.append("-" * 25)
    for category, minutes in categorized_time.items():
        if minutes > 0:
            percentage = (minutes / total_time * 100) if total_time > 0 else 0
            summary.append(f"{category:<20}: {minutes:6.1f}m ({percentage:4.1f}%)")
    
    if uncategorized_time > 0:
        percentage = (uncategorized_time / total_time * 100) if total_time > 0 else 0
        summary.append(f"{'Other':<20}: {uncategorized_time:6.1f}m ({percentage:4.1f}%)")
    
    summary.append("")
    summary.append("Individual Applications:")
    summary.append("-" * 35)
    
    for i, (app, minutes) in enumerate(app_time.head(15).items(), 1):
        percentage = (minutes / total_time * 100) if total_time > 0 else 0
        summary.append(f"{i:2d}. {app:<30} {minutes:6.1f}m ({percentage:4.1f}%)")
    
    return "\n".join(summary)

def start_tracking_background():
    """
    Start tracking in background using thread
    """
    try:
        from screentime_tracker import log_activity
        
        print("[+] Starting background tracking...")
        thread = threading.Thread(target=log_activity, daemon=True)
        thread.start()
        
        print("[+] Screen time tracker is running in background")
        print("    Data is being saved to screentime_data.csv")
        print("    Press Ctrl+C to stop or close terminal")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Background tracking stopped")
    
    except ImportError:
        print("[ERROR] Could not import screentime_tracker module")
    except Exception as e:
        print(f"[ERROR] Failed to start tracking: {e}")

def check_tracking_status():
    """
    Check if tracking is currently running
    """
    try:
        # Check for Python processes running the tracker
        result = subprocess.run([
            'pgrep', '-f', 'screentime_tracker.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"[+] Tracking is RUNNING (PIDs: {', '.join(pids)})")
            return True
        else:
            print("[-] Tracking is NOT running")
            return False
    
    except Exception as e:
        print(f"[ERROR] Could not check status: {e}")
        return False

def stop_tracking():
    """
    Stop background tracking
    """
    try:
        result = subprocess.run([
            'pkill', '-f', 'screentime_tracker.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[+] Background tracking stopped")
        else:
            print("[-] No tracking process found to stop")
    
    except Exception as e:
        print(f"[ERROR] Could not stop tracking: {e}")

def setup_autostart():
    """
    Setup auto-start using macOS LaunchAgent
    """
    try:
        # Get the current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        python_path = sys.executable
        tracker_script = os.path.join(script_dir, 'screentime_tracker.py')
        
        # Create LaunchAgent plist
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.screentime.tracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{tracker_script}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/screentime_tracker.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/screentime_tracker_error.log</string>
</dict>
</plist>'''
        
        # Create LaunchAgents directory if it doesn't exist
        launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents')
        os.makedirs(launch_agents_dir, exist_ok=True)
        
        # Write plist file
        plist_path = os.path.join(launch_agents_dir, 'com.screentime.tracker.plist')
        with open(plist_path, 'w') as f:
            f.write(plist_content)
        
        # Load the launch agent
        subprocess.run(['launchctl', 'load', plist_path], check=True)
        
        print("[+] Auto-start enabled!")
        print(f"    LaunchAgent created at: {plist_path}")
        print("    Tracking will start automatically on login")
        
    except Exception as e:
        print(f"[ERROR] Failed to setup auto-start: {e}")

def remove_autostart():
    """
    Remove auto-start LaunchAgent
    """
    try:
        plist_path = os.path.expanduser('~/Library/LaunchAgents/com.screentime.tracker.plist')
        
        if os.path.exists(plist_path):
            # Unload the launch agent
            subprocess.run(['launchctl', 'unload', plist_path], check=False)
            
            # Remove the plist file
            os.remove(plist_path)
            
            print("[+] Auto-start disabled!")
            print("    LaunchAgent removed")
        else:
            print("[-] Auto-start is not currently enabled")
    
    except Exception as e:
        print(f"[ERROR] Failed to remove auto-start: {e}")

def interactive_menu():
    """
    Show interactive menu for CLI operations
    """
    while True:
        print("\nmacOS Screen Time Tracker - Interactive Menu")
        print("=" * 45)
        print("1. Start tracking in background")
        print("2. Stop tracking")
        print("3. Check tracking status")
        print("4. Today's summary")
        print("5. Weekly report")
        print("6. App usage statistics")
        print("7. Setup auto-start on login")
        print("8. Remove auto-start")
        print("9. Test system compatibility")
        print("0. Exit")
        print("-" * 45)
        
        try:
            choice = input("Select option (0-9): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                start_tracking_background()
            elif choice == '2':
                stop_tracking()
            elif choice == '3':
                check_tracking_status()
            elif choice == '4':
                print("\n" + get_today_summary())
            elif choice == '5':
                print("\n" + get_weekly_summary())
            elif choice == '6':
                print("\n" + get_app_statistics())
            elif choice == '7':
                setup_autostart()
            elif choice == '8':
                remove_autostart()
            elif choice == '9':
                from screentime_tracker import test_system
                test_system()
            else:
                print("Invalid option. Please choose 0-9.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """
    Main CLI entry point
    """
    parser = argparse.ArgumentParser(
        description='macOS Screen Time Tracker - CLI Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 screentime_cli.py                    # Interactive menu
  python3 screentime_cli.py --start            # Start tracking
  python3 screentime_cli.py --today            # Today's report
  python3 screentime_cli.py --weekly           # Weekly report
  python3 screentime_cli.py --apps             # App statistics
        """
    )
    
    parser.add_argument('--start', action='store_true', 
                       help='Start background tracking')
    parser.add_argument('--stop', action='store_true', 
                       help='Stop background tracking')
    parser.add_argument('--status', action='store_true', 
                       help='Check tracking status')
    parser.add_argument('--today', action='store_true', 
                       help='Show today\'s summary')
    parser.add_argument('--weekly', action='store_true', 
                       help='Show weekly report')
    parser.add_argument('--apps', action='store_true', 
                       help='Show app usage statistics')
    parser.add_argument('--autostart', action='store_true', 
                       help='Setup auto-start on login')
    parser.add_argument('--remove-autostart', action='store_true', 
                       help='Remove auto-start')
    parser.add_argument('--test', action='store_true', 
                       help='Test system compatibility')
    
    args = parser.parse_args()
    
    # Handle command line arguments
    if args.start:
        start_tracking_background()
    elif args.stop:
        stop_tracking()
    elif args.status:
        check_tracking_status()
    elif args.today:
        print(get_today_summary())
    elif args.weekly:
        print(get_weekly_summary())
    elif args.apps:
        print(get_app_statistics())
    elif args.autostart:
        setup_autostart()
    elif args.remove_autostart:
        remove_autostart()
    elif args.test:
        from screentime_tracker import test_system
        test_system()
    else:
        # Show interactive menu if no arguments
        interactive_menu()

if __name__ == "__main__":
    main()
