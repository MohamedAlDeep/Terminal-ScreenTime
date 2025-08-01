# Screen Time Tracker - Project Overview

A comprehensive cross-platform screen time tracking application with CLI interface and executable distribution.

## 📁 Project Structure

```
Terminal ScreenTime/
├── Windows Version/
│   ├── screentime_tracker.py      # Windows activity tracking
│   ├── screentime_cli.py          # CLI interface
│   ├── screentime_main.py         # Executable entry point
│   ├── screentime_report.py       # Report generation
│   ├── requirements.txt           # Dependencies
│   ├── screentime.spec            # PyInstaller config
│   └── ScreenTimeTracker.exe      # Built executable
│
├── Linux/
│   ├── Core Files/
│   │   ├── screentime_tracker.py  # Linux tracking (X11/Wayland)
│   │   ├── screentime_cli.py      # CLI interface
│   │   ├── screentime_main.py     # Executable entry point
│   │   └── requirements.txt       # Dependencies
│   │
│   ├── Installation Scripts/
│   │   ├── install_advanced.sh    # Auto-installer with system integration
│   │   ├── setup.sh              # Quick setup
│   │   ├── install.sh            # Dependency installer
│   │   ├── build_executable.sh   # Executable builder
│   │   └── test.sh               # Testing script
│   │
│   ├── Build System/
│   │   ├── Makefile              # Build automation
│   │   └── screentime.spec       # PyInstaller config
│   │
│   ├── System Integration/
│   │   ├── screentime-tracker@.service  # Systemd service
│   │   └── screentime-tracker.desktop   # Desktop entry
│   │
│   └── Documentation/
│       └── README.md             # Comprehensive Linux docs
│
└── Mac/
    ├── Core Files/
    │   ├── screentime_tracker.py  # macOS tracking (AppleScript/IOKit)
    │   ├── screentime_cli.py      # CLI interface
    │   ├── screentime_main.py     # Executable entry point
    │   └── requirements.txt       # Dependencies
    │
    ├── Installation Scripts/
    │   ├── install_advanced.sh    # Auto-installer with app bundle
    │   ├── setup.sh              # Quick setup
    │   ├── install.sh            # Dependency installer
    │   ├── build_executable.sh   # Executable & app bundle builder
    │   └── test.sh               # Testing script
    │
    ├── Build System/
    │   ├── Makefile              # Build automation
    │   └── screentime.spec       # PyInstaller config with app bundle
    │
    └── Documentation/
        └── README.md             # Comprehensive macOS docs
```

## 🎯 Features

### Core Functionality
- **Activity Tracking**: Real-time monitoring of active applications and idle time
- **Cross-Platform**: Native Windows and Linux support
- **Data Storage**: CSV format with UTF-8 encoding
- **Privacy**: Local data storage, no external connections

### CLI Interface
- **Interactive Menu**: User-friendly command-line interface
- **Multiple Reports**: Today, weekly, app usage, productivity analysis
- **Background Tracking**: Daemon mode for continuous monitoring
- **Export Options**: CSV data export and analysis

### Statistics & Analysis
- **Time Tracking**: Detailed time spent per application
- **Productivity Analysis**: Categorized app usage (productive/neutral/unproductive)
- **Usage Patterns**: Daily and weekly trend analysis
- **Idle Time Monitoring**: Screen lock and away time tracking

### Distribution
- **Standalone Executables**: No Python installation required for end users
- **System Integration**: Auto-start services and desktop entries
- **Easy Installation**: Automated installers for both platforms

## 🚀 Quick Start

### Windows
```cmd
# Run the pre-built executable
ScreenTimeTracker.exe

# Or install from source
pip install -r requirements.txt
python screentime_cli.py
```

### Linux
```bash
# Recommended: Advanced auto-installer
chmod +x Linux/install_advanced.sh
./Linux/install_advanced.sh

# Or simple setup
./Linux/setup.sh

# Or manual build
cd Linux/
make executable
```

### macOS
```bash
# Recommended: Advanced auto-installer
chmod +x Mac/install_advanced.sh
./Mac/install_advanced.sh

# Or simple setup
./Mac/setup.sh

# Or manual build
cd Mac/
make executable
```

## 🔧 System Requirements

### Windows
- Windows 7/8/10/11
- Python 3.7+ (for source installation)
- Dependencies: pywin32, psutil, pandas

### Linux
- Any modern Linux distribution
- X11 or Wayland display server
- Python 3.7+ (for source installation)
- System packages: xprop, xprintidle (auto-installed)
- Dependencies: psutil, pandas

### macOS
- macOS 10.14+ (Mojave and later)
- Apple Silicon (M1/M2/M3) and Intel Macs
- Python 3.7+ (for source installation)
- Accessibility permissions required
- System packages: AppleScript, IOKit (built-in)
- Dependencies: psutil, pandas

## 📊 Data Format

The application stores data in CSV format:
```csv
timestamp,idle_seconds,app_name,window_title
2024-01-15 10:30:00,0,Firefox,GitHub - Mozilla Firefox
2024-01-15 10:30:30,0,VSCode,project.py - Visual Studio Code
```

## 🏗️ Architecture

### Windows Implementation
- Uses Win32 APIs for window detection
- psutil for process information
- Built-in screensaver detection

### Linux Implementation
- X11 support via xprop and xwininfo
- Wayland support via compositor-specific tools
- Fallback mechanisms for compatibility
- Display server auto-detection

### macOS Implementation
- Uses AppleScript and IOKit APIs for window detection
- Accessibility permissions for app monitoring
- LaunchAgent integration for auto-start
- App bundle creation for native distribution
- System Events integration for idle detection

### Common Components
- pandas for data analysis
- argparse for CLI interface
- PyInstaller for executable building
- UTF-8 encoding with fallback handling

## 🔄 Development Workflow

1. **Windows Development**: Use Windows APIs and test with ScreenTimeTracker.exe
2. **Linux Development**: Use X11/Wayland tools and test with built executable
3. **macOS Development**: Use AppleScript/IOKit APIs and test with app bundle
4. **Cross-Platform Testing**: Ensure feature parity between platforms
5. **Distribution**: Build executables for easy deployment

## 📈 Future Enhancements

- GUI interface with charts and graphs
- Web dashboard for remote monitoring
- Team/organization reporting features
- Plugin system for custom productivity rules
- Mobile companion app
- Cloud sync capabilities (optional)

## 🤝 Contributing

The project is designed for easy contribution:
- Modular architecture
- Platform-specific implementations
- Comprehensive documentation
- Automated testing and building

Areas for contribution:
- Additional platform support
- Enhanced Wayland integration (Linux)
- Menu bar integration (macOS)
- Performance optimizations
- UI/UX improvements
- Distribution packaging

## 📄 License

This project is available for use and modification. See individual files for specific licensing information.

---

**Total Files**: 35+ files across Windows, Linux, and macOS implementations
**Languages**: Python, Shell scripting, Makefile, AppleScript integration
**Platforms**: Windows 7-11, Linux (X11/Wayland), macOS 10.14+ (Intel/Apple Silicon)
**Architecture**: Modular, cross-platform, executable-ready
