# Screen Time Tracker CLI

A comprehensive Windows screen time tracking and analysis tool with an enhanced CLI interface.

## 🚀 Quick Start Options

### Option 1: Standalone Executable (Recommended)
**No Python installation required!**

```cmd
# Download and run the standalone executable
.\RunScreenTime.bat --today        # Today's summary
.\RunScreenTime.bat --week         # Weekly report
.\RunScreenTime.bat --apps         # App usage statistics
.\RunScreenTime.bat --start        # Start tracking
.\RunScreenTime.bat                # Interactive menu
```

**Executable Features:**
- ✅ **No Dependencies**: Runs on any Windows 10/11 system
- ✅ **Single File**: ~37MB standalone executable
- ✅ **All Features**: Complete functionality included
- ✅ **Easy Distribution**: Share with teams/organization
- ✅ **Desktop Shortcut**: Run `CreateDesktopShortcut.ps1`

### Option 2: Python Installation
For developers or custom modifications:

```bash
# Install dependencies
pip install -r requirements.txt

# Run Python version
python screentime_cli.py --today
```

## Features

### 📊 Tracking
- **Start/Stop Tracking**: Control the background tracking process
- **Status Check**: Verify if tracking is active and check last log time
- **Startup Integration**: Add tracker to Windows startup

### 📈 Statistics & Analysis
- **Today's Summary**: Quick overview of current day activity
- **Weekly Report**: 7-day activity breakdown with daily averages
- **App Usage Statistics**: Detailed app usage with time spent and session counts
- **Productivity Analysis**: Categorizes apps into productive/social/entertainment
- **Custom Date Range**: Analyze any specific time period

### 🔧 Tools
- **Data Export**: Export activity data to CSV with additional analysis columns
- **Data Management**: View settings, clear data, open data folder
- **Multiple Access Methods**: Interactive menu or command-line arguments

## Installation & Usage

### 🎯 Executable Version (No Python Required)

The easiest way to use Screen Time Tracker is with the standalone executable:

1. **Download**: Get `ScreenTimeTracker.exe` from the `dist` folder
2. **Run**: Use the convenient launcher batch file

```cmd
# Basic usage with launcher
.\RunScreenTime.bat --help         # Show all options
.\RunScreenTime.bat --today        # Today's activity summary
.\RunScreenTime.bat --week         # Weekly report
.\RunScreenTime.bat --apps         # App usage statistics
.\RunScreenTime.bat --start        # Start background tracking

# Direct executable usage
dist\ScreenTimeTracker.exe --today
dist\ScreenTimeTracker.exe --apps
```

### 🐍 Python Development Version

For developers who want to modify the code:
```bash
pip install -r requirements.txt
```

### Basic Usage

#### Command Line Interface
```bash
# Start tracking
python screentime_cli.py --start

# Check status
python screentime_cli.py --status

# View today's summary
python screentime_cli.py --today

# View weekly report
python screentime_cli.py --week

# View app usage statistics
python screentime_cli.py --apps

# Stop tracking
python screentime_cli.py --stop
```

#### Batch File (Windows)
```cmd
# Use the batch file for easier access
.\screentime.bat --today
.\screentime.bat --start
.\screentime.bat --apps
```

#### Interactive Menu
```bash
python screentime_cli.py
```
This opens a full interactive menu with all features.

## Configuration

- **Log Location**: `%LOCALAPPDATA%\ScreenTime\activity_log.csv`
- **Log Interval**: 60 seconds
- **Idle Threshold**: 5 minutes (300 seconds)

## Data Structure

The activity log contains:
- `timestamp`: When the activity was recorded
- `idle_seconds`: Time since last user input
- `app_name`: Name of the active application
- `window_title`: Title of the active window

## Productivity Categories

The productivity analysis categorizes apps as:
- **Productive**: Code editors, IDEs, development tools
- **Social**: Browsers, communication apps
- **Entertainment**: Games, media players, streaming

You can customize these categories by editing the `productivity_analysis()` function.

## Export Features

Data can be exported with additional analysis columns:
- `date`: Date of activity
- `hour`: Hour of activity (0-23)
- `day_of_week`: Day name (Monday, Tuesday, etc.)
- `active`: Boolean indicating if user was active

## Command Line Options

### Executable Version
```
usage: ScreenTimeTracker.exe [-h] [--track] [--start] [--stop] [--status] [--today] [--week] [--apps]

Screen Time Tracker - All-in-One

options:
  -h, --help  show this help message and exit
  --track     Start background tracking (blocking)
  --start     Start tracking in background
  --stop      Stop tracking
  --status    Check tracking status
  --today     Show today's summary
  --week      Show weekly report
  --apps      Show app usage statistics
```

### Python CLI Version
```
usage: screentime_cli.py [-h] [--start] [--stop] [--status] [--today] [--week] [--apps]

Screen Time Tracker CLI

options:
  -h, --help  show this help message and exit
  --start     Start tracking in background
  --stop      Stop tracking
  --status    Check tracking status
  --today     Show today's summary
  --week      Show weekly report
  --apps      Show app usage statistics
```

## Requirements

### 🎯 Executable Version
- **Windows OS**: Windows 10/11 (64-bit)
- **No additional requirements**: Completely standalone

### 🐍 Python Development Version
- **Windows OS**: Windows 10/11
- **Python**: 3.7+ (tested with 3.13)
- **Required packages** (see requirements.txt):
  - pandas
  - psutil
  - pywin32
  - comtypes
  - python-dateutil
  - pyinstaller (for building executable)

## File Structure

```
Terminal ScreenTime/
├── dist/
│   └── ScreenTimeTracker.exe      # Standalone executable (37MB)
├── screentime_tracker.py          # Core tracking logic
├── screentime_cli.py              # Enhanced CLI interface
├── screentime_main.py             # Executable entry point
├── screentime_report.py           # Legacy report generator
├── screentime.bat                 # Development batch wrapper
├── RunScreenTime.bat              # Executable launcher
├── CreateDesktopShortcut.ps1      # Desktop shortcut creator
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── EXECUTABLE_README.md           # Executable-specific documentation
```

## Usage Examples

### 🎯 Daily Workflow (Executable)
```cmd
# Morning: Start tracking
.\RunScreenTime.bat --start

# Throughout day: Check status
.\RunScreenTime.bat --status

# Evening: View summary
.\RunScreenTime.bat --today

# Weekly: Generate comprehensive report
.\RunScreenTime.bat --week
```

### 📊 Analysis Workflow (Executable)
```cmd
# Check which apps you use most
.\RunScreenTime.bat --apps

# Interactive analysis (productivity, custom dates, export)
.\RunScreenTime.bat
# Then use menu options for detailed analysis
```

### 🐍 Python Development Workflow
```bash
# Morning: Start tracking
.\screentime.bat --start

# Throughout day: Check status
.\screentime.bat --status

# Evening: View today's summary
.\screentime.bat --today

# Weekly: Generate comprehensive report
.\screentime.bat --week
```

### 🔬 Advanced Analysis (Python)
```bash
# Check which apps you use most
.\screentime.bat --apps

# Run productivity analysis
python screentime_cli.py
# Then select option 7 (Productivity Analysis)

# Export data for external analysis
python screentime_cli.py
# Then select option 10 (Export Data)
```

## Troubleshooting

### Executable Version Issues
1. **Antivirus warnings**: Some antivirus software may flag new executables - add exception if needed
2. **Permission errors**: Run as administrator for startup integration features
3. **Slow first start**: Windows may take time to load the executable initially
4. **Missing executable**: Ensure `ScreenTimeTracker.exe` is in the `dist` folder

### Python Version Issues
1. **Tracker not starting**: Ensure Python and required packages are installed
2. **No data showing**: Make sure tracker has been running and collecting data
3. **Permission errors**: Run as administrator if needed for startup integration
4. **Import errors**: Run `pip install -r requirements.txt` to install dependencies
5. **UTF-8 errors**: Use the latest version with encoding fixes

### General Issues
- **Data location**: Check `%LOCALAPPDATA%\ScreenTime\activity_log.csv`
- **Process conflicts**: Only run one version (executable OR Python) at a time
- **Encoding issues**: Both versions now handle Unicode characters properly

## 📦 Distribution & Sharing

### Executable Distribution
To share the Screen Time Tracker with others:

**Minimal Distribution:**
- `dist/ScreenTimeTracker.exe` (standalone executable)

**Complete Distribution:**
- `dist/ScreenTimeTracker.exe` (main executable)
- `RunScreenTime.bat` (convenient launcher)
- `CreateDesktopShortcut.ps1` (desktop shortcut creator)
- `EXECUTABLE_README.md` (user documentation)

### Building from Source
To create your own executable:
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --name ScreenTimeTracker --console screentime_main.py

# Executable will be created in dist/ folder
```

## Privacy Note

All data is stored locally on your machine in `%LOCALAPPDATA%\ScreenTime\`. No data is sent to external servers.
