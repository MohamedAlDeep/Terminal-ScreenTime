# Linux Screen Time Tracker

A comprehensive Linux screen time tracking and analysis tool with CLI interface and executable distribution.

## 🚀 Quick Start Options

### Option 1: Advanced Auto-Install (Recommended)
**Complete system integration with auto-start and desktop entry**

```bash
chmod +x install_advanced.sh
./install_advanced.sh
```

This automated installer will:
- Detect your Linux distribution
- Install all dependencies automatically
- Build the executable
- Install system-wide (`/usr/local/bin/screentime-tracker`)
- Add desktop application entry
- Setup auto-start service (optional)

### Option 2: Simple Setup Script
```bash
./setup.sh
```

### Option 3: Makefile Build
```bash
make help           # Show all options
make executable     # Install deps and build
make install-system # Install system-wide
make uninstall      # Remove system installation
```

### Option 4: Standalone Executable (Manual)
**No Python setup required after building!**

```bash
# Build the executable (one-time setup)
./install.sh              # Install dependencies
./build_executable.sh     # Build executable

# Use the executable
./dist/screentime-tracker --today    # Today's summary
./dist/screentime-tracker --week     # Weekly report
./dist/screentime-tracker --apps     # App usage statistics
./dist/screentime-tracker --start    # Start tracking
./dist/screentime-tracker            # Interactive menu
```

### Option 2: Python Scripts
For developers or systems without executable support:

```bash
# Install dependencies
./install.sh

# Run Python version
python3 screentime_cli.py --today
```

## 🖥️ System Compatibility

### Display Servers
- ✅ **X11**: Full support with idle detection and window tracking
- ⚠️ **Wayland**: Limited support (app detection may be restricted)
- 🔧 **Fallback**: Process-based tracking when window info unavailable

### Linux Distributions
Tested and supported:
- **Ubuntu/Debian** (apt)
- **Fedora** (dnf)
- **Arch Linux** (pacman)
- **openSUSE** (zypper)
- Other distributions (manual dependency installation)

## Features

### 📊 Tracking
- **Start/Stop Tracking**: Control the background tracking process
- **Status Check**: Verify if tracking is active and check last log time
- **Autostart Integration**: Add tracker to desktop autostart

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

### 🎯 Executable Version (Recommended)

1. **Install Dependencies & Build**:
```bash
./install.sh              # Install system and Python dependencies
./build_executable.sh     # Build the standalone executable
```

2. **Use the Executable**:
```bash
# Basic usage
./dist/screentime-tracker --help         # Show all options
./dist/screentime-tracker --today        # Today's activity summary
./dist/screentime-tracker --week         # Weekly report
./dist/screentime-tracker --apps         # App usage statistics
./dist/screentime-tracker --start        # Start background tracking

# Optional: Install system-wide
sudo cp dist/screentime-tracker /usr/local/bin/
screentime-tracker --today
```

### 🐍 Python Development Version

```bash
# Install dependencies
./install.sh

# Run scripts directly
python3 screentime_cli.py --start
python3 screentime_cli.py --today
python3 screentime_cli.py --apps
python3 screentime_cli.py              # Interactive menu
```

## System Dependencies

### Required Packages
- **xprop**: Window property information (X11)
- **xprintidle**: Idle time detection (X11)

### Optional Packages
- **xssstate**: Enhanced screensaver detection
- **gdbus/qdbus**: Wayland compositor communication
- **swaymsg**: Sway window manager support

### Auto-Installation
The `install.sh` script automatically detects your distribution and installs required packages.

## Configuration

- **Log Location**: `~/.local/share/screentime/activity_log.csv`
- **Log Interval**: 60 seconds
- **Idle Threshold**: 5 minutes (300 seconds)
- **Autostart**: `~/.config/autostart/screentime-tracker.desktop`

## Data Structure

The activity log contains:
- `timestamp`: When the activity was recorded
- `idle_seconds`: Time since last user input
- `app_name`: Name of the active application
- `window_title`: Title of the active window

## Productivity Categories

The productivity analysis categorizes Linux apps as:
- **Productive**: code, vim, emacs, libreoffice, gimp, blender, etc.
- **Social**: firefox, chrome, discord, slack, telegram, etc.
- **Entertainment**: vlc, spotify, steam, minecraft, etc.

You can customize these categories by editing the `productivity_analysis()` function.

## Command Line Options

### Executable Version
```
usage: screentime-tracker [-h] [--track] [--start] [--stop] [--status] [--today] [--week] [--apps]

Linux Screen Time Tracker - All-in-One

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

Linux Screen Time Tracker CLI

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
- **Linux OS**: Any modern distribution
- **Display Server**: X11 (full support) or Wayland (limited)
- **Build Dependencies**: Python 3.7+, pip3, system packages (automated by install.sh)
- **Runtime**: No additional requirements after building

### 🐍 Python Development Version
- **Linux OS**: Any modern distribution
- **Python**: 3.7+ 
- **Required packages** (see requirements.txt):
  - pandas
  - psutil
  - python-dateutil
  - pyinstaller (for building executable)

## File Structure

```
Linux/
├── dist/
│   └── screentime-tracker            # Standalone executable
├── screentime_tracker.py             # Core tracking logic
├── screentime_cli.py                 # Enhanced CLI interface
├── screentime_main.py                # Executable entry point
├── requirements.txt                  # Python dependencies
├── screentime.spec                   # PyInstaller spec file
├── install.sh                        # Dependency installer
├── build_executable.sh               # Executable builder
└── README.md                         # This file
```

## Usage Examples

### 🎯 Daily Workflow (Executable)
```bash
# Morning: Start tracking
./dist/screentime-tracker --start

# Throughout day: Check status
./dist/screentime-tracker --status

# Evening: View summary
./dist/screentime-tracker --today

# Weekly: Generate comprehensive report
./dist/screentime-tracker --week
```

### 📊 Analysis Workflow (Executable)
```bash
# Check which apps you use most
./dist/screentime-tracker --apps

# Interactive analysis (productivity, custom dates, export)
./dist/screentime-tracker
# Then use menu options for detailed analysis
```

### 🐍 Python Development Workflow
```bash
# Morning: Start tracking
python3 screentime_cli.py --start

# Throughout day: Check status
python3 screentime_cli.py --status

# Evening: View today's summary
python3 screentime_cli.py --today

# Weekly: Generate comprehensive report
python3 screentime_cli.py --week
```

## Display Server Notes

### X11 (Full Support)
- ✅ Accurate idle time detection
- ✅ Active window detection
- ✅ Application name resolution
- ✅ Window title capture

### Wayland (Limited Support)
- ⚠️ Idle detection may not work
- ⚠️ Window information restricted by design
- 🔧 Falls back to process-based detection
- 📝 Some compositors provide limited APIs

### Troubleshooting Display Issues
```bash
# Check your display server
echo $XDG_SESSION_TYPE

# X11 troubleshooting
xprop -root _NET_ACTIVE_WINDOW     # Test window detection
xprintidle                         # Test idle detection

# Wayland troubleshooting
# Limited options due to security model
ps aux | grep -E "(gnome|kde|sway)" # Check compositor
```

## Troubleshooting

### Build Issues
1. **Missing dependencies**: Run `./install.sh` to install required packages
2. **PyInstaller fails**: Ensure you have enough disk space and memory
3. **Permission errors**: Make sure you have write permissions in the directory

### Runtime Issues
1. **Tracking not working**: Check if display server is supported
2. **No window detection**: Install xprop and xprintidle for X11
3. **Permission errors**: Some features may require additional permissions
4. **Wayland limitations**: Window tracking is restricted by design

### General Issues
- **Data location**: Check `~/.local/share/screentime/activity_log.csv`
- **Process conflicts**: Only run one instance at a time
- **Log file corruption**: Clear data and restart tracking

## 📦 Distribution & Sharing

### Executable Distribution
To share the Screen Time Tracker:

**Minimal Distribution:**
- `dist/screentime-tracker` (standalone executable)

**Complete Distribution:**
- `dist/screentime-tracker` (main executable)
- `install.sh` (dependency installer)
- `README.md` (documentation)

### Building from Source
```bash
# Clone or copy the Linux folder
cd Linux/

# Install dependencies and build
./install.sh
./build_executable.sh

# Executable will be in dist/
```

## Security & Privacy

- **Local Data**: All data stored locally in `~/.local/share/screentime/`
- **No Network**: No data transmitted over network
- **Wayland Security**: Respects Wayland's security model (limited window access)
- **Process Access**: Uses standard Linux process APIs
- **Permissions**: Runs with user privileges (no root required)

## Contributing

The Linux version is designed to be:
- **Cross-distribution compatible**
- **Display server agnostic**
- **Privacy respecting**
- **Easy to build and distribute**

## 📁 File Structure

### Core Application Files
- `screentime_tracker.py` - Main tracking engine with X11/Wayland support
- `screentime_cli.py` - Command-line interface and statistics
- `screentime_main.py` - Unified entry point for executable
- `requirements.txt` - Python dependencies

### Build and Installation
- `install_advanced.sh` - Complete auto-installer with system integration
- `setup.sh` - Quick setup script
- `install.sh` - Dependency installer
- `build_executable.sh` - Executable builder
- `test.sh` - Testing script
- `Makefile` - Build automation
- `screentime.spec` - PyInstaller configuration

### System Integration
- `screentime-tracker@.service` - Systemd service for auto-start
- `screentime-tracker.desktop` - Desktop application entry
- `README.md` - This documentation

### Generated Files (after build)
- `dist/screentime-tracker` - Standalone executable
- `screentime_data.csv` - Tracking data storage

## 🏗️ Auto-Start Service

After using the advanced installer, you can manage the auto-start service:

```bash
# Check service status
systemctl --user status screentime-tracker@$USER.service

# Stop the service
systemctl --user stop screentime-tracker@$USER.service

# Disable auto-start
systemctl --user disable screentime-tracker@$USER.service

# Re-enable auto-start
systemctl --user enable screentime-tracker@$USER.service
```

Contributions welcome for:
- Additional compositor support
- Better Wayland integration
- Performance improvements
- Distribution packaging
