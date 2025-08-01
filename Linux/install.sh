#!/bin/bash
# Install dependencies for Linux Screen Time Tracker

echo "Installing Linux Screen Time Tracker dependencies..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "Fedora: sudo dnf install python3 python3-pip"
    echo "Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    echo "Ubuntu/Debian: sudo apt install python3-pip"
    echo "Fedora: sudo dnf install python3-pip"
    echo "Arch: sudo pacman -S python-pip"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install system dependencies based on distribution
echo "Installing system dependencies..."

if command -v apt &> /dev/null; then
    # Ubuntu/Debian
    echo "Detected Ubuntu/Debian system"
    sudo apt update
    sudo apt install -y x11-utils xprintidle
    echo "Optional: Install xssstate for better screensaver detection"
    echo "sudo apt install xssstate"
    
elif command -v dnf &> /dev/null; then
    # Fedora
    echo "Detected Fedora system"
    sudo dnf install -y xorg-x11-utils xprintidle
    
elif command -v pacman &> /dev/null; then
    # Arch Linux
    echo "Detected Arch Linux system"
    sudo pacman -S --noconfirm xorg-xprop xprintidle
    
elif command -v zypper &> /dev/null; then
    # openSUSE
    echo "Detected openSUSE system"
    sudo zypper install -y xprop xprintidle
    
else
    echo "Unknown distribution. Please install the following packages manually:"
    echo "- xprop (usually in xorg-x11-utils or similar)"
    echo "- xprintidle"
    echo "- Optional: xssstate (for screensaver detection)"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  ./screentime_cli.py --help          # Show help"
echo "  ./screentime_cli.py --start         # Start tracking"
echo "  ./screentime_cli.py --today         # Today's summary"
echo "  ./screentime_cli.py                 # Interactive menu"
echo ""
echo "To build executable:"
echo "  ./build_executable.sh"
