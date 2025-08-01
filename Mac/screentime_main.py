#!/usr/bin/env python3
"""
macOS Screen Time Tracker - All-in-One Executable
Main entry point that handles both tracking and CLI functionality
"""
import os
import sys
import subprocess
import argparse
import threading
import time

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    parser = argparse.ArgumentParser(description='macOS Screen Time Tracker - All-in-One')
    parser.add_argument('--track', action='store_true', help='Start background tracking')
    parser.add_argument('--cli', action='store_true', help='Open CLI interface')
    parser.add_argument('--start', action='store_true', help='Start tracking in background')
    parser.add_argument('--stop', action='store_true', help='Stop tracking')
    parser.add_argument('--status', action='store_true', help='Check tracking status')
    parser.add_argument('--today', action='store_true', help='Show today\'s summary')
    parser.add_argument('--weekly', action='store_true', help='Show weekly report')
    parser.add_argument('--apps', action='store_true', help='Show app usage statistics')
    parser.add_argument('--autostart', action='store_true', help='Setup auto-start on login')
    parser.add_argument('--remove-autostart', action='store_true', help='Remove auto-start')
    parser.add_argument('--test', action='store_true', help='Test system compatibility')
    parser.add_argument('--background', action='store_true', help='Start tracking in background mode')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help and start CLI
    if len(sys.argv) == 1:
        print("macOS Screen Time Tracker - All-in-One Executable")
        print("=" * 50)
        print("Usage options:")
        print("  --track         Start background tracking")
        print("  --cli           Open CLI interface")
        print("  --start         Start tracking")
        print("  --stop          Stop tracking")
        print("  --status        Check status")
        print("  --today         Today's summary")
        print("  --weekly        Weekly report")
        print("  --apps          App usage stats")
        print("  --autostart     Setup auto-start")
        print("  --test          Test compatibility")
        print("\nStarting CLI interface...")
        time.sleep(2)
        args.cli = True
    
    if args.track or args.background:
        # Start tracker in background
        from screentime_tracker import log_activity
        print("[+] Starting background tracking...")
        thread = threading.Thread(target=log_activity, daemon=True)
        thread.start()
        
        print("[+] Tracker is running in background")
        print("    Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[+] Tracker stopped")
            
    elif args.cli or args.start or args.stop or args.status or args.today or args.weekly or args.apps or args.autostart or args.remove_autostart or args.test:
        # Import and run CLI
        from screentime_cli import main as cli_main
        
        # If specific CLI arguments, modify sys.argv for the CLI
        if not args.cli:
            new_argv = ['screentime_cli.py']
            if args.start:
                new_argv.append('--start')
            elif args.stop:
                new_argv.append('--stop')
            elif args.status:
                new_argv.append('--status')
            elif args.today:
                new_argv.append('--today')
            elif args.weekly:
                new_argv.append('--weekly')
            elif args.apps:
                new_argv.append('--apps')
            elif args.autostart:
                new_argv.append('--autostart')
            elif args.remove_autostart:
                new_argv.append('--remove-autostart')
            elif args.test:
                new_argv.append('--test')
            
            original_argv = sys.argv
            sys.argv = new_argv
            try:
                cli_main()
            finally:
                sys.argv = original_argv
        else:
            # Run interactive CLI
            cli_main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
