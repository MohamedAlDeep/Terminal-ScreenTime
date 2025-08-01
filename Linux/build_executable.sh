#!/bin/bash
# Build Linux Screen Time Tracker executable

echo "Building Linux Screen Time Tracker executable..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip3 install pyinstaller
fi

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ __pycache__/

# Build the executable
echo "Building executable with PyInstaller..."
pyinstaller --onefile \
    --name screentime-tracker \
    --console \
    --clean \
    screentime_main.py

# Check if build was successful
if [ -f "dist/screentime-tracker" ]; then
    echo ""
    echo "Build successful!"
    echo "Executable created: dist/screentime-tracker"
    echo ""
    
    # Make executable
    chmod +x dist/screentime-tracker
    
    # Test the executable
    echo "Testing executable..."
    ./dist/screentime-tracker --help
    
    echo ""
    echo "Usage:"
    echo "  ./dist/screentime-tracker --help     # Show help"
    echo "  ./dist/screentime-tracker --start    # Start tracking"
    echo "  ./dist/screentime-tracker --today    # Today's summary"
    echo "  ./dist/screentime-tracker            # Interactive menu"
    echo ""
    echo "To install system-wide (optional):"
    echo "  sudo cp dist/screentime-tracker /usr/local/bin/"
    echo "  screentime-tracker --help"
    
else
    echo "Build failed! Check the output above for errors."
    exit 1
fi
