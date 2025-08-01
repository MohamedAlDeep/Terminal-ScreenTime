# Screen Time Tracker - Executable Distribution

## 🎯 Single Executable Solution

Your Screen Time Tracker has been successfully compiled into a single executable file that requires **no Python installation**!

## 📁 Files

- **`dist/ScreenTimeTracker.exe`** - Main executable (standalone)
- **`RunScreenTime.bat`** - Convenient launcher for PowerShell
- **`ScreenTime.bat`** - Legacy launcher (for development)

## 🚀 Quick Start

### Option 1: Direct Executable
```cmd
# Navigate to the dist folder and run directly
cd dist
ScreenTimeTracker.exe --help
ScreenTimeTracker.exe --today
ScreenTimeTracker.exe --start
```

### Option 2: Using Launcher (Recommended)
```cmd
# Use the convenient launcher from the main folder
.\RunScreenTime.bat --help
.\RunScreenTime.bat --today
.\RunScreenTime.bat --start
```

## 📊 Available Commands

```cmd
# Quick statistics
.\RunScreenTime.bat --today        # Today's summary
.\RunScreenTime.bat --week         # Weekly report
.\RunScreenTime.bat --apps         # App usage statistics
.\RunScreenTime.bat --status       # Check if tracking is active

# Tracking control
.\RunScreenTime.bat --start        # Start background tracking
.\RunScreenTime.bat --stop         # Stop tracking
.\RunScreenTime.bat --track        # Start tracker (blocking mode)

# Interactive menu
.\RunScreenTime.bat                # Open full interactive menu
```

## 📦 Deployment

### Single File Distribution
The `ScreenTimeTracker.exe` file is completely self-contained:
- ✅ No Python installation required
- ✅ No dependencies to install
- ✅ All libraries bundled inside
- ✅ Works on any Windows 10/11 system

### Distribution Package
To share with others, provide:
1. `dist/ScreenTimeTracker.exe` (main file)
2. `RunScreenTime.bat` (optional launcher)
3. This README file

## 🔧 Features

All original features are included in the executable:
- ✅ Background activity tracking
- ✅ Today's activity summary
- ✅ Weekly reports with daily breakdown
- ✅ Detailed app usage statistics
- ✅ Productivity analysis
- ✅ Custom date range analysis
- ✅ Data export functionality
- ✅ Settings management
- ✅ Windows startup integration

## 📈 Usage Examples

### Daily Workflow
```cmd
# Morning: Start tracking
.\RunScreenTime.bat --start

# Throughout day: Check status
.\RunScreenTime.bat --status

# Evening: View summary
.\RunScreenTime.bat --today
```

### Weekly Analysis
```cmd
# Check weekly patterns
.\RunScreenTime.bat --week

# Detailed app usage
.\RunScreenTime.bat --apps

# Full interactive analysis
.\RunScreenTime.bat
# Then use menu options 7-8 for productivity analysis
```

## 💾 Data Storage

The executable uses the same data location as the original:
- **Location**: `%LOCALAPPDATA%\ScreenTime\activity_log.csv`
- **Format**: CSV with timestamp, idle time, app name, window title
- **Privacy**: All data stays on your local machine

## 🎯 Advantages of Executable Version

1. **Portability**: Run on any Windows system without Python
2. **Simplicity**: Single file distribution
3. **Performance**: Optimized startup time
4. **Deployment**: Easy to share with team/organization
5. **Reliability**: No dependency conflicts

## 🔍 File Sizes

- **Executable**: ~50-70 MB (includes Python runtime + all libraries)
- **Data files**: Minimal (CSV logs grow over time)

## ⚙️ Technical Details

- **Built with**: PyInstaller
- **Target**: Windows x64
- **Dependencies**: All bundled (pandas, psutil, pywin32, etc.)
- **Console Application**: For maximum compatibility

## 🛠️ Troubleshooting

1. **Antivirus warnings**: Some antivirus may flag new executables - add exception if needed
2. **Permission errors**: Run as administrator for startup integration features
3. **Data location**: Use `--help` to see all available commands

## 📝 Notes

- The executable is larger than the Python scripts but completely standalone
- First run may be slightly slower as Windows loads the executable
- All original functionality is preserved
- Data format remains compatible with the Python version
