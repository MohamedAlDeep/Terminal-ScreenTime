#!/bin/bash

# macOS Screen Time Tracker - Dependency Installer
# Installs Python dependencies required for the tracker

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

print_status "macOS Screen Time Tracker - Installing Dependencies"
echo "=================================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only!"
    exit 1
fi

# Check macOS version
macos_version=$(sw_vers -productVersion)
print_status "macOS Version: $macos_version"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    print_status "Please install Python 3 from:"
    print_status "  - https://www.python.org/downloads/"
    print_status "  - Or use Homebrew: brew install python3"
    exit 1
fi

python_version=$(python3 --version)
print_status "Found: $python_version"

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed!"
    print_status "Installing pip3..."
    python3 -m ensurepip --upgrade
fi

# Upgrade pip
print_status "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install required packages
print_status "Installing Python packages..."

if python3 -m pip install -r requirements.txt; then
    print_success "Python packages installed successfully!"
else
    print_error "Failed to install some packages"
    print_status "Trying individual installation..."
    
    packages=("pandas" "psutil" "pyinstaller")
    
    for package in "${packages[@]}"; do
        print_status "Installing $package..."
        if python3 -m pip install "$package"; then
            print_success "$package installed"
        else
            print_warning "Failed to install $package"
        fi
    done
fi

# Check if all packages are available
print_status "Verifying installation..."

python3 -c "
import sys
packages = ['pandas', 'psutil']
missing = []

for package in packages:
    try:
        __import__(package)
        print(f'✓ {package}')
    except ImportError:
        print(f'✗ {package}')
        missing.append(package)

if missing:
    print(f'Missing packages: {missing}')
    sys.exit(1)
else:
    print('All required packages are available!')
"

if [ $? -eq 0 ]; then
    print_success "Installation completed successfully!"
    echo
    print_status "You can now run:"
    print_status "  python3 screentime_tracker.py --test    # Test system"
    print_status "  python3 screentime_cli.py               # Interactive CLI"
    print_status "  ./build_executable.sh                   # Build executable"
else
    print_error "Installation verification failed!"
    exit 1
fi
