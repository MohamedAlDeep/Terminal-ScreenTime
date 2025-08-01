#!/bin/bash
# Test script for Linux Screen Time Tracker

echo "Testing Linux Screen Time Tracker..."
echo "===================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
else
    echo "✅ Python 3 found: $(python3 --version)"
fi

# Check if required Python modules can be imported
echo "Testing Python dependencies..."
python3 -c "
try:
    import pandas
    print('✅ pandas imported successfully')
except ImportError:
    print('❌ pandas not found - run ./install.sh')
    exit(1)

try:
    import psutil
    print('✅ psutil imported successfully')
except ImportError:
    print('❌ psutil not found - run ./install.sh')
    exit(1)

try:
    from datetime import datetime
    import os
    print('✅ Core modules imported successfully')
except ImportError:
    print('❌ Core modules import failed')
    exit(1)
"

# Check display server
echo "Display server information:"
if [ -n "$WAYLAND_DISPLAY" ]; then
    echo "🟡 Wayland detected - limited functionality"
    echo "   WAYLAND_DISPLAY: $WAYLAND_DISPLAY"
elif [ -n "$DISPLAY" ]; then
    echo "✅ X11 detected - full functionality"
    echo "   DISPLAY: $DISPLAY"
    
    # Test X11 tools
    if command -v xprop &> /dev/null; then
        echo "✅ xprop available"
    else
        echo "❌ xprop not found - install x11-utils"
    fi
    
    if command -v xprintidle &> /dev/null; then
        echo "✅ xprintidle available"
    else
        echo "❌ xprintidle not found - install xprintidle"
    fi
else
    echo "❓ Unknown display server"
fi

# Test script execution
echo ""
echo "Testing script execution..."

# Test CLI help
echo "Testing CLI help..."
if python3 screentime_cli.py --help > /dev/null 2>&1; then
    echo "✅ CLI script runs successfully"
else
    echo "❌ CLI script failed"
fi

# Test tracker script syntax
echo "Testing tracker script syntax..."
if python3 -m py_compile screentime_tracker.py; then
    echo "✅ Tracker script syntax OK"
else
    echo "❌ Tracker script syntax error"
fi

# Test main script syntax
echo "Testing main script syntax..."
if python3 -m py_compile screentime_main.py; then
    echo "✅ Main script syntax OK"
else
    echo "❌ Main script syntax error"
fi

echo ""
echo "Test complete!"
echo ""
echo "Next steps:"
echo "1. If any tests failed, run: ./install.sh"
echo "2. To build executable: ./build_executable.sh"
echo "3. To start tracking: python3 screentime_cli.py --start"
