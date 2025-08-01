#!/bin/bash

# macOS Screen Time Tracker - Quick Setup
# One-command setup for the entire tracker

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

echo "macOS Screen Time Tracker - Quick Setup"
echo "======================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only!"
    exit 1
fi

# Make scripts executable
print_status "Making scripts executable..."
chmod +x *.sh

# Run installation
print_status "Installing dependencies..."
./install.sh

# Build executable
print_status "Building executable..."
./build_executable.sh

# Run tests
print_status "Running tests..."
./test.sh

echo
print_success "Setup completed successfully!"
echo
print_status "The macOS Screen Time Tracker is ready to use!"
echo
print_status "Quick start options:"
print_status "  ./dist/screentime-tracker                # Start interactive CLI"
print_status "  ./dist/screentime-tracker --start        # Start background tracking"
print_status "  ./dist/screentime-tracker --today        # View today's summary"
echo
print_status "For the app bundle:"
if [ -d "dist/ScreenTimeTracker.app" ]; then
    print_status "  open dist/ScreenTimeTracker.app          # Launch GUI app"
fi
echo
print_status "Python version (for development):"
print_status "  python3 screentime_cli.py                # Interactive CLI"
