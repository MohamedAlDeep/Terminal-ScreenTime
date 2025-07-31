import os
import sys
import subprocess
import argparse
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser

# Fix encoding issues
if sys.platform == 'win32':
    # For Windows console
    os.system('chcp 65001 > nul')  # Set console to UTF-8

# Configuration
LOG_FILE = os.path.join(os.getenv('LOCALAPPDATA'), 'ScreenTime', 'activity_log.csv')

def show_menu():
    print("\n" + "=" * 60)
    print("SCREEN TIME TRACKER & ANALYZER")
    print("=" * 60)
    print("TRACKING:")
    print("  1. Start/Stop Tracking")
    print("  2. Check Tracking Status")
    print("  3. Add to Startup")
    print("\nSTATISTICS:")
    print("  4. Today's Summary")
    print("  5. Weekly Report")
    print("  6. App Usage Statistics")
    print("  7. Productivity Analysis")
    print("  8. Custom Date Range")
    print("\nTOOLS:")
    print("  9. Open Data Folder")
    print(" 10. Export Data")
    print(" 11. Settings")
    print("  0. Exit")
    print("=" * 60)
    
    choice = input("Choose an option: ")
    return choice

def start_tracking():
    # Check if already running
    try:
        output = subprocess.check_output('tasklist | findstr python', shell=True, text=True)
        if 'screentime_tracker.py' in output.lower():
            print("\n[!] Tracker is already running!")
            choice = input("Do you want to stop it? (y/n): ")
            if choice.lower() == 'y':
                subprocess.run('taskkill /f /im python.exe', shell=True)
                print("[+] Tracker stopped.")
            return
    except:
        pass
    
    # Start the tracker
    subprocess.Popen([sys.executable, "screentime_tracker.py"], 
                     creationflags=subprocess.CREATE_NO_WINDOW)
    print("\n[+] Tracker started in background!")
    print("    It will automatically log your activity.")

def check_tracking_status():
    try:
        output = subprocess.check_output('tasklist | findstr python', shell=True, text=True)
        if 'python' in output.lower():
            print("\n[+] Tracking is ACTIVE")
            # Check last log entry
            if os.path.exists(LOG_FILE):
                df = pd.read_csv(LOG_FILE)
                if not df.empty:
                    last_entry = pd.to_datetime(df['timestamp'].iloc[-1])
                    time_diff = datetime.now() - last_entry
                    if time_diff.total_seconds() < 120:  # Less than 2 minutes
                        print(f"    Last activity logged: {last_entry.strftime('%H:%M:%S')}")
                    else:
                        print(f"    [!] Last log was {int(time_diff.total_seconds()/60)} minutes ago")
        else:
            print("\n[-] Tracking is NOT ACTIVE")
    except:
        print("\n[?] Unable to check tracking status")

def add_to_startup():
    if sys.platform == 'win32':
        try:
            from win32com.client import Dispatch
            startup_dir = os.path.join(
                os.getenv('APPDATA'),
                'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
            )
            shortcut_path = os.path.join(startup_dir, "ScreenTimeTracker.lnk")
            
            if os.path.exists(shortcut_path):
                print("\n[+] Already added to startup!")
                return
                
            target = sys.executable
            script = os.path.join(os.getcwd(), "screentime_tracker.py")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.Arguments = f'"{script}"'
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.save()
            
            print("\n[+] Added to Windows startup!")
            print("    Tracker will automatically start when you log in.")
        except Exception as e:
            print(f"\n[-] Failed to add to startup: {e}")
    else:
        print("\n[-] Startup setup only available on Windows")

def load_data():
    if not os.path.exists(LOG_FILE):
        print("\n[-] No data found. Start the tracker first!")
        return None
    
    try:
        # Try different encodings to handle UTF-8 issues
        encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-8-sig']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(LOG_FILE, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print("\n[-] Unable to read data file due to encoding issues")
            return None
            
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['active'] = df['idle_seconds'] < 300  # 5 minutes threshold
        return df
    except Exception as e:
        print(f"\n[-] Error loading data: {e}")
        return None

def format_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def today_summary():
    df = load_data()
    if df is None:
        return
    
    today = datetime.now().date()
    today_data = df[df['timestamp'].dt.date == today]
    
    if today_data.empty:
        print(f"\n[i] No activity recorded for today ({today})")
        return
    
    active_minutes = today_data['active'].sum()
    unique_apps = today_data[today_data['active']]['app_name'].nunique()
    
    print(f"\nTODAY'S SUMMARY ({today})")
    print("=" * 40)
    print(f"Active Time: {format_time(active_minutes)}")
    print(f"Apps Used: {unique_apps}")
    
    # Top apps today
    if today_data['active'].any():
        top_apps = today_data[today_data['active']].groupby('app_name').size().sort_values(ascending=False).head(5)
        print(f"\nMost Used Apps:")
        for app, count in top_apps.items():
            print(f"  - {app}: {count} minutes")

def weekly_report():
    df = load_data()
    if df is None:
        return
    
    week_ago = datetime.now() - timedelta(days=7)
    week_data = df[df['timestamp'] > week_ago]
    
    if week_data.empty:
        print("\n[i] No activity recorded in the last 7 days")
        return
    
    # Daily breakdown
    daily_stats = week_data.groupby(week_data['timestamp'].dt.date).agg(
        active_minutes=('active', 'sum'),
        unique_apps=('app_name', lambda x: x[week_data.loc[x.index, 'active']].nunique())
    ).reset_index()
    
    print(f"\nWEEKLY REPORT (Last 7 Days)")
    print("=" * 50)
    for _, row in daily_stats.iterrows():
        day_name = pd.to_datetime(row['timestamp']).strftime('%A')
        print(f"{day_name} ({row['timestamp']}): {format_time(row['active_minutes'])} | {row['unique_apps']} apps")
    
    total_time = week_data['active'].sum()
    avg_daily = total_time / 7
    print(f"\nTotal: {format_time(total_time)} | Daily Average: {format_time(avg_daily)}")

def app_usage_stats():
    df = load_data()
    if df is None:
        return
    
    week_ago = datetime.now() - timedelta(days=7)
    recent_data = df[df['timestamp'] > week_ago]
    
    if recent_data.empty:
        print("\n[i] No recent activity data")
        return
    
    app_stats = recent_data[recent_data['active']].groupby('app_name').agg(
        usage_minutes=('active', 'sum'),
        last_used=('timestamp', 'max'),
        sessions=('timestamp', 'count')
    ).sort_values('usage_minutes', ascending=False)
    
    print(f"\nAPP USAGE STATISTICS (Last 7 Days)")
    print("=" * 60)
    print(f"{'App Name':<25} {'Time':<10} {'Sessions':<10} {'Last Used'}")
    print("-" * 60)
    
    for app, row in app_stats.head(15).iterrows():
        last_used = row['last_used'].strftime('%m/%d %H:%M')
        print(f"{app[:24]:<25} {format_time(row['usage_minutes']):<10} {row['sessions']:<10} {last_used}")

def productivity_analysis():
    df = load_data()
    if df is None:
        return
    
    # Define productivity categories (you can customize these)
    productive_apps = ['code.exe', 'notepad++.exe', 'sublime_text.exe', 'atom.exe', 
                      'pycharm64.exe', 'devenv.exe', 'git.exe']
    social_apps = ['chrome.exe', 'firefox.exe', 'discord.exe', 'telegram.exe', 
                  'whatsapp.exe', 'slack.exe']
    entertainment_apps = ['spotify.exe', 'vlc.exe', 'netflix.exe', 'youtube.exe',
                         'steam.exe', 'epicgameslauncher.exe']
    
    week_ago = datetime.now() - timedelta(days=7)
    recent_data = df[df['timestamp'] > week_ago]
    
    if recent_data.empty:
        print("\n[i] No recent activity data")
        return
    
    active_data = recent_data[recent_data['active']]
    
    productive_time = active_data[active_data['app_name'].str.lower().isin([app.lower() for app in productive_apps])]['active'].sum()
    social_time = active_data[active_data['app_name'].str.lower().isin([app.lower() for app in social_apps])]['active'].sum()
    entertainment_time = active_data[active_data['app_name'].str.lower().isin([app.lower() for app in entertainment_apps])]['active'].sum()
    total_time = active_data['active'].sum()
    other_time = total_time - productive_time - social_time - entertainment_time
    
    print(f"\nPRODUCTIVITY ANALYSIS (Last 7 Days)")
    print("=" * 50)
    if total_time > 0:
        print(f"Productive: {format_time(productive_time)} ({productive_time/total_time*100:.1f}%)")
        print(f"Social/Communication: {format_time(social_time)} ({social_time/total_time*100:.1f}%)")
        print(f"Entertainment: {format_time(entertainment_time)} ({entertainment_time/total_time*100:.1f}%)")
        print(f"Other: {format_time(other_time)} ({other_time/total_time*100:.1f}%)")
        print(f"\nTotal Active Time: {format_time(total_time)}")
        
        # Productivity score
        productivity_score = (productive_time / total_time * 100) if total_time > 0 else 0
        if productivity_score >= 70:
            print(f"Productivity Score: {productivity_score:.1f}% - Excellent!")
        elif productivity_score >= 50:
            print(f"Productivity Score: {productivity_score:.1f}% - Good")
        elif productivity_score >= 30:
            print(f"Productivity Score: {productivity_score:.1f}% - Average")
        else:
            print(f"Productivity Score: {productivity_score:.1f}% - Needs Improvement")
    else:
        print("No active time recorded")

def custom_date_range():
    print("\nCustom Date Range Analysis")
    print("Enter dates in YYYY-MM-DD format")
    
    try:
        start_date = input("Start date: ")
        end_date = input("End date: ")
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        
        df = load_data()
        if df is None:
            return
        
        filtered_data = df[(df['timestamp'] >= start_dt) & (df['timestamp'] < end_dt)]
        
        if filtered_data.empty:
            print(f"\n[-] No data found for the period {start_date} to {end_date}")
            return
        
        total_minutes = filtered_data['active'].sum()
        unique_apps = filtered_data[filtered_data['active']]['app_name'].nunique()
        days_span = (end_dt - start_dt).days
        
        print(f"\nANALYSIS ({start_date} to {end_date})")
        print("=" * 50)
        print(f"Total Active Time: {format_time(total_minutes)}")
        print(f"Unique Apps: {unique_apps}")
        print(f"Days Analyzed: {days_span}")
        print(f"Daily Average: {format_time(total_minutes / days_span if days_span > 0 else 0)}")
        
        # Top apps in this period
        if filtered_data['active'].any():
            top_apps = filtered_data[filtered_data['active']].groupby('app_name').size().sort_values(ascending=False).head(10)
            print(f"\nTop Apps in this period:")
            for app, minutes in top_apps.items():
                print(f"  - {app}: {format_time(minutes)}")
                
    except ValueError:
        print("[-] Invalid date format. Please use YYYY-MM-DD")
    except Exception as e:
        print(f"[-] Error: {e}")

def export_data():
    if not os.path.exists(LOG_FILE):
        print("\n[-] No data to export")
        return
    
    try:
        # Create exports directory
        export_dir = os.path.join(os.path.dirname(LOG_FILE), 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_file = os.path.join(export_dir, f'screentime_export_{timestamp}.csv')
        
        # Copy file with additional analysis
        df = load_data()
        if df is not None:
            df['date'] = df['timestamp'].dt.date
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df.to_csv(export_file, index=False)
            
            print(f"\n[+] Data exported to: {export_file}")
            print(f"Total records: {len(df)}")
            
            # Open folder
            subprocess.Popen(f'explorer "{export_dir}"')
        
    except Exception as e:
        print(f"[-] Export failed: {e}")

def open_data_folder():
    data_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'ScreenTime')
    os.makedirs(data_dir, exist_ok=True)
    subprocess.Popen(f'explorer "{data_dir}"')
    print(f"\n[+] Opened data folder: {data_dir}")

def settings():
    print(f"\nSETTINGS")
    print("=" * 30)
    print(f"Data Location: {LOG_FILE}")
    print(f"Data Size: {os.path.getsize(LOG_FILE) / 1024:.1f} KB" if os.path.exists(LOG_FILE) else "No data file")
    
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        print(f"Total Records: {len(df)}")
        print(f"First Record: {df['timestamp'].iloc[0] if not df.empty else 'N/A'}")
        print(f"Last Record: {df['timestamp'].iloc[-1] if not df.empty else 'N/A'}")
    
    print(f"\nConfiguration:")
    print(f"  - Log Interval: 60 seconds")
    print(f"  - Idle Threshold: 5 minutes")
    
    choice = input("\nOptions: (o)pen data folder, (c)lear data, (b)ack: ")
    if choice.lower() == 'o':
        open_data_folder()
    elif choice.lower() == 'c':
        confirm = input("[!] Delete all data? This cannot be undone! (yes/no): ")
        if confirm.lower() == 'yes':
            try:
                os.remove(LOG_FILE)
                print("[+] All data cleared!")
            except:
                print("[-] Failed to clear data")
        else:
            print("[-] Operation cancelled")

def main():
    # Add command line arguments support
    parser = argparse.ArgumentParser(description='Screen Time Tracker CLI')
    parser.add_argument('--start', action='store_true', help='Start tracking in background')
    parser.add_argument('--stop', action='store_true', help='Stop tracking')
    parser.add_argument('--status', action='store_true', help='Check tracking status')
    parser.add_argument('--today', action='store_true', help='Show today\'s summary')
    parser.add_argument('--week', action='store_true', help='Show weekly report')
    parser.add_argument('--apps', action='store_true', help='Show app usage statistics')
    
    args = parser.parse_args()
    
    # Handle command line arguments
    if args.start:
        start_tracking()
        return
    elif args.stop:
        subprocess.run('taskkill /f /im python.exe', shell=True)
        print("[+] Tracker stopped.")
        return
    elif args.status:
        check_tracking_status()
        return
    elif args.today:
        today_summary()
        return
    elif args.week:
        weekly_report()
        return
    elif args.apps:
        app_usage_stats()
        return
    
    # Interactive menu
    try:
        while True:
            choice = show_menu()
            
            if choice == '1':
                start_tracking()
            elif choice == '2':
                check_tracking_status()
            elif choice == '3':
                add_to_startup()
            elif choice == '4':
                today_summary()
            elif choice == '5':
                weekly_report()
            elif choice == '6':
                app_usage_stats()
            elif choice == '7':
                productivity_analysis()
            elif choice == '8':
                custom_date_range()
            elif choice == '9':
                open_data_folder()
            elif choice == '10':
                export_data()
            elif choice == '11':
                settings()
            elif choice == '0':
                print("\nGoodbye!")
                break
            else:
                print("\n[-] Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\n[-] Error: {e}")

if __name__ == "__main__":
    main()
