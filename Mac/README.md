# macOS Screen Time Tracker

A comprehensive macOS screen time tracking and analysis tool with CLI interface and executable distribution.

## 🚀 Quick Start Options

### Option 1: Quick Setup (Recommended)
**Complete installation with one command**

```bash
./setup.sh
```

This will:
- Install all dependencies
- Build the standalone executable
- Run compatibility tests
- Create both CLI and app bundle versions

### Option 2: Makefile Build
```bash
make help           # Show all options
make executable     # Install deps and build
make app           # Build macOS app bundle
make install-system # Install system-wide
```

### Option 3: Manual Setup
```bash
chmod +x *.sh
./install.sh              # Install dependencies
./build_executable.sh     # Build executable
./test.sh                 # Test installation
```

### Option 4: Python Development
```bash
./install.sh              # Install dependencies
python3 screentime_cli.py  # Interactive CLI
```

## 📱 Usage

### Standalone Executable
```bash
# Interactive menu
./dist/screentime-tracker

# Quick commands
./dist/screentime-tracker --today         # Today's summary
./dist/screentime-tracker --weekly        # Weekly report
./dist/screentime-tracker --apps          # App usage stats
./dist/screentime-tracker --start         # Start tracking
./dist/screentime-tracker --autostart     # Setup auto-start
```

### macOS App Bundle
```bash
# Launch GUI app
open dist/ScreenTimeTracker.app

# Or run from terminal
./dist/ScreenTimeTracker.app/Contents/MacOS/screentime-tracker
```

### Python Scripts
For developers or customization:

```bash
python3 screentime_cli.py --today     # Today's report
python3 screentime_tracker.py         # Start tracking
python3 screentime_main.py --help     # All options
```

## 🖥️ System Compatibility

### Supported macOS Versions
- **macOS 10.14 Mojave** and later
- **Apple Silicon (M1/M2/M3)** and Intel Macs
- **macOS Monterey/Ventura/Sonoma** fully supported

### Required Permissions
The app requires **Accessibility permissions** to track active applications:

1. Go to **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility** from the left sidebar
3. Click the lock icon and enter your password
4. Add Terminal or the app to the allowed list

### System Requirements
- **Python 3.7+** (for source installation)
- **AppleScript support** (built into macOS)
- **System commands**: `osascript`, `ioreg`, `pmset`

## 🎯 Features

### Activity Tracking
- **Real-time monitoring** of active applications
- **Window title tracking** for detailed analysis
- **Idle time detection** using macOS APIs
- **Screen lock detection** and screensaver monitoring
- **Background tracking** with minimal CPU usage

### Statistics & Reports
- **Today's Summary**: Current day activity breakdown
- **Weekly Reports**: 7-day trend analysis with daily breakdown
- **App Usage Statistics**: Detailed per-application time tracking
- **Productivity Analysis**: Categorized app usage (productive/entertainment/system)
- **Export capabilities**: CSV data for further analysis

### macOS Integration
- **LaunchAgent support** for auto-start on login
- **App bundle creation** for native macOS distribution
- **System notifications** (optional)
- **Accessibility API integration**
- **AppleScript automation**

## 📊 Data Storage

Data is stored in CSV format in the current directory:
```csv
timestamp,idle_seconds,app_name,window_title
2024-01-15 10:30:00,0,Safari,GitHub - Safari
2024-01-15 10:30:30,0,Xcode,project.swift - Xcode
```

## 🔧 Technical Implementation

### macOS-Specific Features
- **AppleScript integration** for window detection
- **IORegistry access** for hardware idle time
- **Power management APIs** for screen lock detection
- **LaunchAgent integration** for system services
- **App bundle packaging** with proper entitlements

### Tracking Methods
1. **Primary**: AppleScript System Events for active application
2. **Fallback**: `lsappinfo` command for app information
3. **Alternative**: Process list analysis via `ps`

### Idle Detection
1. **Primary**: IOHIDSystem registry for hardware idle time
2. **Fallback**: Power management system queries
3. **Alternative**: Screensaver detection

## 🏗️ Build System

### Building Executable
```bash
# Install build dependencies
./install.sh

# Build standalone executable
./build_executable.sh

# Creates: dist/screentime-tracker (CLI)
# Creates: dist/ScreenTimeTracker.app (App Bundle)
```

### Build Configuration
- **PyInstaller** for executable creation
- **App bundle** with proper macOS structure
- **Entitlements** for system access
- **Universal binary** support (Intel + Apple Silicon)

## 🔄 Auto-Start Setup

### Enable Auto-Start
```bash
./dist/screentime-tracker --autostart
```

This creates a LaunchAgent that:
- Starts tracking automatically on login
- Runs in the background
- Logs to `/tmp/screentime_tracker.log`
- Can be managed via System Preferences

### Manage Auto-Start
```bash
# Check status
launchctl list | grep screentime

# Stop service
launchctl unload ~/Library/LaunchAgents/com.screentime.tracker.plist

# Start service
launchctl load ~/Library/LaunchAgents/com.screentime.tracker.plist

# Remove auto-start
./dist/screentime-tracker --remove-autostart
```

## 📈 Productivity Categories

Apps are automatically categorized for productivity analysis:

### Development Tools
- Xcode, Terminal, VSCode, PyCharm, IntelliJ IDEA
- Sublime Text, Atom, Eclipse, Git clients

### Office/Productivity
- Pages, Numbers, Keynote
- Microsoft Office suite
- TextEdit, Calculator

### Design Tools
- Adobe Creative Suite (Photoshop, Illustrator)
- Sketch, Figma, Canva

### Web Browsing
- Safari, Chrome, Firefox, Edge

### Communication
- Mail, Messages, Slack, Discord, Zoom, Teams

### Entertainment
- YouTube, Netflix, Spotify, Music, Games

### System Tools
- Finder, System Preferences, Activity Monitor

## 🧪 Testing

### System Compatibility Test
```bash
./test.sh
# or
python3 screentime_tracker.py --test
```

Tests include:
- macOS version detection
- Required command availability
- Python package verification
- AppleScript functionality
- Idle time detection
- App detection capabilities

## 🎨 Customization

### Adding Custom App Categories
Edit `screentime_cli.py` and modify the `categories` dictionary:

```python
categories = {
    'Custom Category': ['App Name', 'Another App'],
    'Development': ['Xcode', 'Terminal', 'VSCode'],
    # ... existing categories
}
```

### Adjusting Tracking Interval
Modify the sleep interval in `screentime_tracker.py`:

```python
time.sleep(5)  # Check every 5 seconds (default)
```

### Custom Data Export
```python
import pandas as pd
df = pd.read_csv('screentime_data.csv')
# Custom analysis here
```

## 🚨 Troubleshooting

### Common Issues

**"Permission denied" errors:**
- Grant Accessibility permissions in System Preferences
- Run with `sudo` if needed for system-wide installation

**"osascript not found" errors:**
- AppleScript is disabled - enable in System Preferences
- Try running from Terminal.app directly

**"No data available" messages:**
- Ensure tracking has been running
- Check file permissions on `screentime_data.csv`
- Verify the tracker has Accessibility permissions

**App detection not working:**
- Grant Terminal accessibility permissions
- Some apps may not be detectable (sandboxed apps)
- Try running the executable instead of Python script

### Debug Mode
```bash
python3 screentime_tracker.py --test  # System compatibility
python3 screentime_cli.py --status    # Check tracking status
```

## 📁 File Structure

### Core Application Files
- `screentime_tracker.py` - Main tracking engine with macOS APIs
- `screentime_cli.py` - Command-line interface and statistics
- `screentime_main.py` - Unified entry point for executable
- `requirements.txt` - Python dependencies

### Build and Installation
- `setup.sh` - Quick setup script
- `install.sh` - Dependency installer
- `build_executable.sh` - Executable builder
- `test.sh` - Testing script
- `Makefile` - Build automation
- `screentime.spec` - PyInstaller configuration

### Generated Files (after build)
- `dist/screentime-tracker` - Standalone CLI executable
- `dist/ScreenTimeTracker.app` - macOS app bundle
- `screentime_data.csv` - Tracking data storage

## 🔒 Privacy & Security

- **Local data only** - no network connections
- **CSV file storage** - human-readable format
- **User control** - start/stop tracking anytime
- **Accessibility permissions** - required for app detection
- **No keystroke logging** - only app names and window titles

## 🤝 Contributing

The macOS implementation uses standard Apple APIs and is designed for easy contribution:

- **AppleScript integration** for system events
- **Objective-C runtime** access via Python
- **IOKit framework** for hardware information
- **LaunchServices** for app management

Areas for contribution:
- Enhanced app categorization
- Menu bar integration
- Notification support
- Time limits and alerts
- iCloud sync capabilities

## 📄 License

This project is available for use and modification. See individual files for specific licensing information.

---

**Platform**: macOS 10.14+ (Intel & Apple Silicon)  
**Languages**: Python, AppleScript, Shell scripting  
**Architecture**: Modular, executable-ready, native macOS integration
