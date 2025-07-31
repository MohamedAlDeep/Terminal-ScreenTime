import os
import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser

# Configuration
LOG_FILE = os.path.join(os.getenv('LOCALAPPDATA'), 'ScreenTime', 'activity_log.csv')
REPORT_DAYS = 7  # Days to include in report

def load_data():
    if not os.path.exists(LOG_FILE):
        print("No data found. Start the tracker first!")
        return None
    return pd.read_csv(LOG_FILE)

def generate_report(df):
    # Convert and filter data
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    cutoff = datetime.now() - timedelta(days=REPORT_DAYS)
    df = df[df['timestamp'] > cutoff]
    
    # Create time-based features
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['active'] = df['idle_seconds'] < 300  # 5 minutes
    
    # Calculate statistics
    daily_stats = df.groupby('date').agg(
        active_minutes=('active', 'sum'),
        unique_apps=('app_name', pd.Series.nunique)
    ).reset_index()
    
    app_stats = df[df['active']].groupby('app_name').agg(
        usage_minutes=('active', 'sum'),
        last_used=('timestamp', 'max')
    ).sort_values('usage_minutes', ascending=False).head(10)
    
    hourly_usage = df[df['active']].groupby('hour')['active'].sum().reset_index()
    
    return {
        'daily': daily_stats,
        'apps': app_stats,
        'hourly': hourly_usage,
        'total_minutes': df['active'].sum()
    }

def format_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"

def print_report(report):
    print("\n" + "=" * 50)
    print(f"🖥️  SCREEN TIME REPORT (Last {REPORT_DAYS} Days)")
    print("=" * 50)
    
    # Daily Summary
    print("\n📅 DAILY SUMMARY:")
    for _, row in report['daily'].iterrows():
        print(f"- {row['date']}: {format_time(row['active_minutes'])} "
              f"| Apps: {row['unique_apps']}")
    
    # App Usage
    print("\n🚀 TOP APPLICATIONS:")
    for app, row in report['apps'].iterrows():
        print(f"- {app}: {format_time(row['usage_minutes'])} "
              f"(Last: {row['last_used'].strftime('%Y-%m-%d %H:%M')})")
    
    # Hourly Distribution
    print("\n🕒 HOURLY USAGE PATTERN:")
    for _, row in report['hourly'].iterrows():
        hour = f"{row['hour']:02d}:00"
        print(f"- {hour}: {'▇' * int(row['active'] // 5)}")
    
    # Total
    print("\n" + "-" * 50)
    print(f"TOTAL ACTIVE TIME: {format_time(report['total_minutes'])}")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        report = generate_report(df)
        print_report(report)