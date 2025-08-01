#!/bin/bash

# Advanced Installation Script for Linux Screen Time Tracker
# Includes system-wide installation and auto-start setup

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

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root!"
        print_status "Please run as a normal user. The script will ask for sudo when needed."
        exit 1
    fi
}

# Detect distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    else
        print_error "Cannot detect Linux distribution!"
        exit 1
    fi
    print_status "Detected: $PRETTY_NAME"
}

# Install dependencies based on distribution
install_dependencies() {
    print_status "Installing dependencies for $DISTRO..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv x11-utils xprintidle
            ;;
        fedora)
            sudo dnf install -y python3 python3-pip xorg-x11-utils xprintidle
            ;;
        centos|rhel)
            sudo yum install -y python3 python3-pip xorg-x11-utils
            # xprintidle might need EPEL
            ;;
        arch)
            sudo pacman -Sy python python-pip xorg-xprop xprintidle
            ;;
        opensuse*)
            sudo zypper install python3 python3-pip xprop xprintidle
            ;;
        *)
            print_warning "Unknown distribution. Please install manually:"
            print_status "- python3 and pip3"
            print_status "- xprop (from x11-utils)"
            print_status "- xprintidle"
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
            ;;
    esac
}

# Install Python packages
install_python_packages() {
    print_status "Installing Python packages..."
    pip3 install --user -r requirements.txt
}

# Build executable
build_executable() {
    print_status "Building executable..."
    ./build_executable.sh
    if [[ ! -f "dist/screentime-tracker" ]]; then
        print_error "Executable build failed!"
        exit 1
    fi
}

# Install system-wide
install_system_wide() {
    print_status "Installing executable system-wide..."
    sudo cp dist/screentime-tracker /usr/local/bin/
    sudo chmod +x /usr/local/bin/screentime-tracker
    
    print_status "Installing desktop entry..."
    sudo cp screentime-tracker.desktop /usr/share/applications/
    sudo chmod 644 /usr/share/applications/screentime-tracker.desktop
    
    print_success "System-wide installation complete!"
}

# Setup auto-start
setup_autostart() {
    read -p "Do you want to enable auto-start on login? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Setting up auto-start..."
        
        # Copy systemd service
        sudo cp screentime-tracker@.service /etc/systemd/system/
        
        # Enable for current user
        sudo systemctl daemon-reload
        sudo systemctl enable screentime-tracker@$USER.service
        
        print_success "Auto-start enabled! Tracker will start on next login."
        
        read -p "Start tracker now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo systemctl start screentime-tracker@$USER.service
            print_success "Tracker started!"
        fi
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    if /usr/local/bin/screentime-tracker --help > /dev/null 2>&1; then
        print_success "Installation test passed!"
    else
        print_error "Installation test failed!"
        exit 1
    fi
}

# Show completion message
show_completion() {
    echo
    print_success "Installation completed successfully!"
    echo
    print_status "Usage:"
    print_status "  screentime-tracker                 - Interactive CLI"
    print_status "  screentime-tracker --today         - Today's report"
    print_status "  screentime-tracker --weekly        - Weekly report"
    print_status "  screentime-tracker --background    - Start tracking"
    echo
    print_status "Files created:"
    print_status "  /usr/local/bin/screentime-tracker"
    print_status "  /usr/share/applications/screentime-tracker.desktop"
    if systemctl is-enabled screentime-tracker@$USER.service >/dev/null 2>&1; then
        print_status "  Auto-start service enabled"
    fi
    echo
    print_status "To uninstall, run: make uninstall"
}

# Main installation flow
main() {
    echo "Linux Screen Time Tracker - Advanced Installer"
    echo "=============================================="
    
    check_root
    detect_distro
    install_dependencies
    install_python_packages
    build_executable
    install_system_wide
    setup_autostart
    test_installation
    show_completion
}

# Run main function
main "$@"
