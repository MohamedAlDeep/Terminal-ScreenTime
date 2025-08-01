#!/bin/bash

# macOS Screen Time Tracker - Executable Builder
# Builds standalone executable using PyInstaller

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

print_status "macOS Screen Time Tracker - Building Executable"
echo "=============================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only!"
    exit 1
fi

# Check if required files exist
required_files=("screentime_main.py" "screentime_tracker.py" "screentime_cli.py" "requirements.txt")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file not found: $file"
        exit 1
    fi
done

print_success "All required files found"

# Check if Python packages are installed
print_status "Checking Python dependencies..."

python3 -c "
import sys
try:
    import pandas
    import psutil
    import PyInstaller
    print('✓ All required packages available')
except ImportError as e:
    print(f'✗ Missing package: {e}')
    print('Run ./install.sh first')
    sys.exit(1)
" || exit 1

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ __pycache__/ *.pyc
rm -f *.spec~

# Build executable using PyInstaller
print_status "Building executable with PyInstaller..."

if pyinstaller screentime.spec --clean --noconfirm; then
    print_success "Executable built successfully!"
else
    print_error "Build failed!"
    exit 1
fi

# Check if executable was created
if [ -f "dist/screentime-tracker" ]; then
    print_success "Standalone executable created: dist/screentime-tracker"
    
    # Make executable
    chmod +x dist/screentime-tracker
    
    # Test the executable
    print_status "Testing executable..."
    if dist/screentime-tracker --help > /dev/null 2>&1; then
        print_success "Executable test passed!"
    else
        print_warning "Executable test failed, but file exists"
    fi
    
    # Show file size
    size=$(du -h dist/screentime-tracker | cut -f1)
    print_status "Executable size: $size"
    
elif [ -d "dist/ScreenTimeTracker.app" ]; then
    print_success "macOS App bundle created: dist/ScreenTimeTracker.app"
    
    # Test the app bundle
    print_status "Testing app bundle..."
    if dist/ScreenTimeTracker.app/Contents/MacOS/screentime-tracker --help > /dev/null 2>&1; then
        print_success "App bundle test passed!"
    else
        print_warning "App bundle test failed, but bundle exists"
    fi
    
    # Show bundle size
    size=$(du -sh dist/ScreenTimeTracker.app | cut -f1)
    print_status "App bundle size: $size"
    
else
    print_error "No executable found after build!"
    exit 1
fi

echo
print_success "Build completed successfully!"
echo
print_status "Usage:"
if [ -f "dist/screentime-tracker" ]; then
    print_status "  ./dist/screentime-tracker                 # Interactive CLI"
    print_status "  ./dist/screentime-tracker --today         # Today's report"
    print_status "  ./dist/screentime-tracker --weekly        # Weekly report"
    print_status "  ./dist/screentime-tracker --start         # Start tracking"
fi

if [ -d "dist/ScreenTimeTracker.app" ]; then
    print_status "  Open dist/ScreenTimeTracker.app           # Launch app"
    print_status "  Or run from terminal:"
    print_status "  ./dist/ScreenTimeTracker.app/Contents/MacOS/screentime-tracker"
fi

echo
print_status "The executable is standalone and doesn't require Python!"
print_status "You can copy the dist/ folder to other macOS machines."
