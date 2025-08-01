# Makefile for macOS Screen Time Tracker

.PHONY: help install test build clean run executable install-system uninstall app

help:
	@echo "macOS Screen Time Tracker - Makefile"
	@echo "====================================="
	@echo "Available targets:"
	@echo "  install        - Install dependencies"
	@echo "  test          - Test installation"
	@echo "  build         - Build executable"
	@echo "  app           - Build macOS app bundle"
	@echo "  executable    - Install deps and build"
	@echo "  run           - Run CLI interactively"
	@echo "  clean         - Clean build files"
	@echo "  install-system - Install executable system-wide"
	@echo "  uninstall     - Remove system-wide installation"

install:
	@echo "Installing dependencies..."
	./install.sh

test:
	@echo "Testing installation..."
	./test.sh

build:
	@echo "Building executable..."
	./build_executable.sh

app: build
	@echo "App bundle ready at dist/ScreenTimeTracker.app"

executable: install test build
	@echo "Complete build finished!"

run:
	@echo "Starting interactive CLI..."
	python3 screentime_cli.py

clean:
	@echo "Cleaning build files..."
	rm -rf build/ dist/ __pycache__/ *.pyc
	rm -f *.spec~

install-system: build
	@echo "Installing system-wide..."
	sudo cp dist/screentime-tracker /usr/local/bin/
	@echo "Installed to /usr/local/bin/screentime-tracker"

uninstall:
	@echo "Removing system-wide installation..."
	sudo rm -f /usr/local/bin/screentime-tracker
	@echo "Uninstalled from /usr/local/bin/"
