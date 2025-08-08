# Screen Time Tracker - Standalone Executable

A completely standalone Windows executable for tracking and analyzing your screen time. **No Python installation required!**

## 🚀 Quick Start

Simply download `ScreenTimeTracker.exe` and run it from anywhere on your Windows system.

### Basic Usage

```cmd
# Show help
ScreenTimeTracker.exe --help

# Start tracking in background
ScreenTimeTracker.exe --start

# Check if tracking is running
ScreenTimeTracker.exe --status

# View today's summary
ScreenTimeTracker.exe --today

# Stop tracking
ScreenTimeTracker.exe --stop
```

### Interactive Mode

```cmd
# Run without arguments for interactive menu
ScreenTimeTracker.exe
```

## 📊 Features

### Activity Tracking
- **Real-time monitoring** of active applications and windows
- **Idle time detection** when you're away from your computer
- **Screen lock detection** for accurate activity logging
- **Background operation** with minimal system impact

### Reports & Statistics
- **Today's Summary**: Current day activity breakdown
- **Weekly Reports**: 7-day activity analysis
- **App Usage Statistics**: Time spent per application
- **Productivity Analysis**: Categorized app usage

### Data Management
- **CSV data storage** in the same folder as the executable
- **UTF-8 encoding** for international character support
- **Privacy-focused**: All data stays on your computer

## 🎯 Commands

| Command | Description |
|---------|-------------|
| `--help` | Show all available options |
| `--start` | Start background tracking |
| `--stop` | Stop background tracking |
| `--status` | Check if tracking is running |
| `--today` | Show today's activity summary |
| `--week` | Show weekly activity report |
| `--apps` | Show application usage statistics |
| `--track` | Start tracking in foreground (for testing) |

## 📁 File Structure

When you run the executable, it creates these files in the same directory:

```
ScreenTimeTracker.exe       # The main executable
screentime_data.csv         # Your activity data
screentime.lock             # Lock file (when tracking is active)
```

## 🔧 Installation & Setup

### No Installation Required!
1. Download `ScreenTimeTracker.exe`
2. Place it in any folder you prefer
3. Run it from Command Prompt or PowerShell

### Optional: Add to System PATH
To run from anywhere:
1. Place `ScreenTimeTracker.exe` in a folder like `C:\Tools\`
2. Add that folder to your Windows PATH environment variable
3. Now you can run `ScreenTimeTracker --today` from any directory

### Optional: Auto-Start with Windows
To automatically start tracking when you log in:
1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a shortcut to `ScreenTimeTracker.exe --start`
3. Tracking will start automatically on login

## 💡 Usage Examples

### Daily Workflow
```cmd
# Morning: Start tracking
ScreenTimeTracker.exe --start

# During day: Check status occasionally
ScreenTimeTracker.exe --status

# Evening: View summary
ScreenTimeTracker.exe --today

# Weekend: Check weekly stats
ScreenTimeTracker.exe --week
```

### First Time Setup
```cmd
# 1. Test the executable
ScreenTimeTracker.exe --help

# 2. Start tracking for the first time
ScreenTimeTracker.exe --start

# 3. Let it run for a while, then check
ScreenTimeTracker.exe --status

# 4. View your first report
ScreenTimeTracker.exe --today
```

## 📈 Data Analysis

### CSV Data Format
Your activity data is stored in `screentime_data.csv` with these columns:
- `timestamp`: When the activity was recorded
- `idle_seconds`: How long you were idle
- `app_name`: Name of the active application
- `window_title`: Title of the active window

### Example Data
```csv
timestamp,idle_seconds,app_name,window_title
2024-01-15 09:30:00,0,chrome.exe,GitHub - Google Chrome
2024-01-15 09:30:05,0,notepad.exe,Document.txt - Notepad
2024-01-15 09:30:10,300,chrome.exe,GitHub - Google Chrome
```

### Opening in Excel
You can open `screentime_data.csv` directly in Microsoft Excel or Google Sheets for custom analysis.

## 🛠️ Troubleshooting

### Common Issues

**"The executable doesn't start"**
- Make sure you're running on Windows 7 or later
- Try running as Administrator if needed
- Check Windows Defender hasn't quarantined the file

**"No data is being recorded"**
- Make sure tracking is started: `ScreenTimeTracker.exe --start`
- Check status: `ScreenTimeTracker.exe --status`
- Wait a few minutes, then check: `ScreenTimeTracker.exe --today`

**"Status shows 'NOT ACTIVE' but I started tracking"**
- The background process might have stopped
- Restart tracking: `ScreenTimeTracker.exe --start`
- Check if antivirus software is blocking the process

**"Permission denied errors"**
- Run Command Prompt as Administrator
- Make sure the executable has write permissions in its folder

### Getting Help

**Check if it's working:**
```cmd
ScreenTimeTracker.exe --status
```

**View recent activity:**
```cmd
ScreenTimeTracker.exe --today
```

**Reset everything:**
1. Stop tracking: `ScreenTimeTracker.exe --stop`
2. Delete `screentime_data.csv` and `screentime.lock`
3. Start fresh: `ScreenTimeTracker.exe --start`

## 🔒 Privacy & Security

- **Local Data Only**: No internet connection required or used
- **Your Computer**: All data stays on your machine
- **No Keylogging**: Only tracks window titles and app names
- **User Control**: You can start/stop tracking anytime
- **Open Data**: CSV format you can read and analyze yourself

## 📋 System Requirements

- **Windows 7** or later (Windows 10/11 recommended)
- **64-bit Windows** (most modern systems)
- **~100MB disk space** for the executable and data
- **Minimal RAM/CPU usage** when running in background

## 🎁 What's Included

This standalone executable includes:
- Complete activity tracking engine
- Statistical analysis capabilities
- Command-line interface
- Data export functionality
- All necessary dependencies bundled in

**No Python, no additional software, no complex setup required!**

---

**File Size**: ~100MB (includes all dependencies)  
**Platform**: Windows 7/8/10/11 (64-bit)  
**License**: Free for personal use  
**Version**: Standalone 2.0
