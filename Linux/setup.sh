#!/bin/bash
# Quick setup script for Linux Screen Time Tracker
# This script will install dependencies and build the executable in one go

set -e  # Exit on any error

echo "Linux Screen Time Tracker - Quick Setup"
echo "======================================="

# Make scripts executable
chmod +x *.sh
chmod +x *.py

# Run installation
echo "Step 1: Installing dependencies..."
./install.sh

echo ""
echo "Step 2: Testing installation..."
./test.sh

echo ""
echo "Step 3: Building executable..."
./build_executable.sh

echo ""
echo "Setup complete! 🎉"
echo ""
echo "Quick usage:"
echo "  ./dist/screentime-tracker --help     # Show help"
echo "  ./dist/screentime-tracker --start    # Start tracking"
echo "  ./dist/screentime-tracker --today    # Today's summary"
echo "  ./dist/screentime-tracker            # Interactive menu"
echo ""
echo "To install system-wide:"
echo "  sudo cp dist/screentime-tracker /usr/local/bin/"
echo "  screentime-tracker --help"
