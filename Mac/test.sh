#!/bin/bash

# macOS Screen Time Tracker - Test Script
# Tests installation and basic functionality

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

print_status "macOS Screen Time Tracker - Testing Installation"
echo "=============================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only!"
    exit 1
fi

# Test Python installation
print_status "Testing Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    print_success "Python found: $python_version"
else
    print_error "Python 3 not found!"
    exit 1
fi

# Test required files
print_status "Checking required files..."
required_files=("screentime_tracker.py" "screentime_cli.py" "screentime_main.py" "requirements.txt")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_error "✗ $file (missing)"
        exit 1
    fi
done

# Test Python packages
print_status "Testing Python packages..."
python3 -c "
import sys
packages = [
    ('pandas', 'Data analysis'),
    ('psutil', 'System utilities'),
]

all_good = True
for package, description in packages:
    try:
        __import__(package)
        print(f'✓ {package:<10} - {description}')
    except ImportError:
        print(f'✗ {package:<10} - {description} (NOT INSTALLED)')
        all_good = False

if not all_good:
    print('Run ./install.sh to install missing packages')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Test system compatibility
print_status "Testing system compatibility..."
python3 screentime_tracker.py --test

if [ $? -eq 0 ]; then
    print_success "System compatibility test passed!"
else
    print_warning "System compatibility issues detected"
fi

# Test CLI functionality
print_status "Testing CLI help..."
if python3 screentime_cli.py --help > /dev/null 2>&1; then
    print_success "CLI help works"
else
    print_error "CLI help failed"
    exit 1
fi

# Test main entry point
print_status "Testing main entry point..."
if python3 screentime_main.py --help > /dev/null 2>&1; then
    print_success "Main entry point works"
else
    print_error "Main entry point failed"
    exit 1
fi

# Test executable if it exists
if [ -f "dist/screentime-tracker" ]; then
    print_status "Testing standalone executable..."
    if dist/screentime-tracker --help > /dev/null 2>&1; then
        print_success "Standalone executable works"
    else
        print_warning "Standalone executable test failed"
    fi
elif [ -d "dist/ScreenTimeTracker.app" ]; then
    print_status "Testing app bundle..."
    if dist/ScreenTimeTracker.app/Contents/MacOS/screentime-tracker --help > /dev/null 2>&1; then
        print_success "App bundle works"
    else
        print_warning "App bundle test failed"
    fi
else
    print_status "No executable found (run ./build_executable.sh to create one)"
fi

# Quick functionality test
print_status "Running quick functionality test..."
timeout 10s python3 -c "
from screentime_tracker import get_foreground_app, get_idle_time, get_system_info

# Test basic functions
try:
    app, window = get_foreground_app()
    print(f'Current app: {app}')
    
    idle = get_idle_time()
    print(f'Idle time: {idle} seconds')
    
    info = get_system_info()
    print(f'System: {info[\"platform\"]} {info[\"version\"]}')
    
    print('Basic functionality test passed!')
except Exception as e:
    print(f'Functionality test failed: {e}')
    import sys
    sys.exit(1)
" || print_warning "Quick functionality test failed or timed out"

echo
print_success "All tests completed!"
echo
print_status "Ready to use:"
print_status "  python3 screentime_cli.py               # Interactive CLI"
print_status "  python3 screentime_tracker.py           # Start tracking"
print_status "  python3 screentime_cli.py --today       # Today's summary"

if [ -f "dist/screentime-tracker" ]; then
    echo
    print_status "Standalone executable available:"
    print_status "  ./dist/screentime-tracker               # Interactive CLI"
    print_status "  ./dist/screentime-tracker --today       # Today's summary"
elif [ -d "dist/ScreenTimeTracker.app" ]; then
    echo
    print_status "App bundle available:"
    print_status "  Open dist/ScreenTimeTracker.app         # Launch app"
fi
