#!/bin/bash

# Advanced Installation Script for macOS Screen Time Tracker
# Includes system-wide installation, auto-start setup, and app bundle creation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS only!"
        print_status "Current OS: $OSTYPE"
        exit 1
    fi
}

# Detect macOS version
detect_macos_version() {
    macos_version=$(sw_vers -productVersion)
    macos_name=$(sw_vers -productName)
    
    print_status "Detected: $macos_name $macos_version"
    
    # Check if version is supported
    major_version=$(echo "$macos_version" | cut -d. -f1)
    minor_version=$(echo "$macos_version" | cut -d. -f2)
    
    if [[ $major_version -lt 10 ]] || [[ $major_version -eq 10 && $minor_version -lt 14 ]]; then
        print_warning "macOS $macos_version may not be fully supported"
        print_status "Recommended: macOS 10.14 or later"
        
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check and install Python
install_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version)
        print_success "Found: $python_version"
    else
        print_warning "Python 3 not found!"
        print_status "Installing Python 3..."
        
        # Check if Homebrew is available
        if command -v brew &> /dev/null; then
            print_status "Using Homebrew to install Python..."
            brew install python3
        else
            print_error "Python 3 installation required!"
            print_status "Please install Python 3 from:"
            print_status "  - https://www.python.org/downloads/"
            print_status "  - Or install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    fi
    
    # Ensure pip is available
    if ! command -v pip3 &> /dev/null; then
        print_status "Installing pip..."
        python3 -m ensurepip --upgrade
    fi
}

# Install Python packages
install_python_packages() {
    print_status "Installing Python packages..."
    
    # Upgrade pip first
    python3 -m pip install --upgrade pip
    
    # Install packages
    if python3 -m pip install -r requirements.txt; then
        print_success "Python packages installed successfully!"
    else
        print_warning "Some packages failed to install, trying individually..."
        
        packages=("pandas" "psutil" "pyinstaller")
        for package in "${packages[@]}"; do
            print_status "Installing $package..."
            python3 -m pip install "$package" || print_warning "Failed to install $package"
        done
    fi
}

# Check system requirements
check_system_requirements() {
    print_status "Checking system requirements..."
    
    # Check required commands
    commands=("osascript" "ioreg" "pmset" "sw_vers" "launchctl")
    missing_commands=()
    
    for cmd in "${commands[@]}"; do
        if command -v "$cmd" &> /dev/null; then
            print_success "✓ $cmd"
        else
            print_error "✗ $cmd (required)"
            missing_commands+=("$cmd")
        fi
    done
    
    if [ ${#missing_commands[@]} -ne 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_status "These are usually part of macOS. You may need to install Xcode Command Line Tools:"
        print_status "  xcode-select --install"
        exit 1
    fi
}

# Build executable
build_executable() {
    print_status "Building executable..."
    
    # Make build script executable
    chmod +x build_executable.sh
    
    # Run build
    if ./build_executable.sh; then
        print_success "Executable built successfully!"
    else
        print_error "Executable build failed!"
        exit 1
    fi
}

# Install system-wide
install_system_wide() {
    read -p "Do you want to install the executable system-wide? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Installing executable system-wide..."
        
        if [ -f "dist/screentime-tracker" ]; then
            sudo cp dist/screentime-tracker /usr/local/bin/
            sudo chmod +x /usr/local/bin/screentime-tracker
            print_success "Installed to /usr/local/bin/screentime-tracker"
        else
            print_error "Executable not found!"
            return 1
        fi
    fi
}

# Install app bundle
install_app_bundle() {
    if [ -d "dist/ScreenTimeTracker.app" ]; then
        read -p "Do you want to install the app bundle to Applications? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Installing app bundle..."
            
            # Copy to Applications folder
            cp -R dist/ScreenTimeTracker.app /Applications/
            print_success "App bundle installed to /Applications/ScreenTimeTracker.app"
            
            # Register with Launch Services
            /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f /Applications/ScreenTimeTracker.app
            
            print_status "You can now find 'ScreenTimeTracker' in your Applications folder"
        fi
    fi
}

# Setup auto-start
setup_autostart() {
    read -p "Do you want to enable auto-start on login? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setting up auto-start..."
        
        # Use the CLI to setup auto-start
        if [ -f "dist/screentime-tracker" ]; then
            dist/screentime-tracker --autostart
            print_success "Auto-start enabled!"
        elif command -v /usr/local/bin/screentime-tracker &> /dev/null; then
            /usr/local/bin/screentime-tracker --autostart
            print_success "Auto-start enabled!"
        else
            python3 screentime_cli.py --autostart
            print_success "Auto-start enabled!"
        fi
        
        print_status "Tracking will start automatically on next login"
    fi
}

# Check permissions
check_permissions() {
    print_status "Checking Accessibility permissions..."
    
    # Try to get the frontmost app to test permissions
    if osascript -e 'tell application "System Events" to get name of first application process whose frontmost is true' &> /dev/null; then
        print_success "Accessibility permissions are granted"
    else
        print_warning "Accessibility permissions may be required"
        print_status "To grant permissions:"
        print_status "1. Go to System Preferences → Security & Privacy → Privacy"
        print_status "2. Select 'Accessibility' from the left sidebar"
        print_status "3. Click the lock and enter your password"
        print_status "4. Add Terminal (or the app) to the allowed list"
        
        read -p "Continue without permissions? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Please grant permissions and run the installer again"
            exit 1
        fi
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Make test script executable
    chmod +x test.sh
    
    # Run tests
    if ./test.sh; then
        print_success "Installation test passed!"
    else
        print_warning "Some tests failed, but installation may still work"
    fi
}

# Show completion message
show_completion() {
    echo
    print_success "Installation completed successfully!"
    echo
    print_status "🎉 macOS Screen Time Tracker is ready!"
    echo
    
    print_status "Usage options:"
    
    if command -v /usr/local/bin/screentime-tracker &> /dev/null; then
        print_status "  screentime-tracker                   # Interactive CLI"
        print_status "  screentime-tracker --today           # Today's report"
        print_status "  screentime-tracker --start           # Start tracking"
    fi
    
    if [ -f "dist/screentime-tracker" ]; then
        print_status "  ./dist/screentime-tracker            # Local executable"
    fi
    
    if [ -f "/Applications/ScreenTimeTracker.app/Contents/MacOS/screentime-tracker" ]; then
        print_status "  Open 'ScreenTimeTracker' from Applications folder"
    fi
    
    print_status "  python3 screentime_cli.py            # Python version"
    
    echo
    print_status "Files created:"
    [ -f "/usr/local/bin/screentime-tracker" ] && print_status "  /usr/local/bin/screentime-tracker (system-wide)"
    [ -d "/Applications/ScreenTimeTracker.app" ] && print_status "  /Applications/ScreenTimeTracker.app (app bundle)"
    [ -f "$HOME/Library/LaunchAgents/com.screentime.tracker.plist" ] && print_status "  Auto-start service enabled"
    
    echo
    print_status "To uninstall:"
    print_status "  sudo rm -f /usr/local/bin/screentime-tracker"
    print_status "  rm -rf /Applications/ScreenTimeTracker.app"
    print_status "  launchctl unload ~/Library/LaunchAgents/com.screentime.tracker.plist"
    print_status "  rm -f ~/Library/LaunchAgents/com.screentime.tracker.plist"
}

# Main installation flow
main() {
    echo "macOS Screen Time Tracker - Advanced Installer"
    echo "=============================================="
    
    check_macos
    detect_macos_version
    install_python
    check_system_requirements
    install_python_packages
    build_executable
    install_system_wide
    install_app_bundle
    check_permissions
    setup_autostart
    test_installation
    show_completion
}

# Run main function
main "$@"
