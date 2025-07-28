"""
Main Application File for Portal System
Entry point for the console-based portal system
"""

import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system_manager import SystemManager
from utils.menu_manager import MenuManager


def get_yes_no_input(prompt: str) -> bool:
    """
    Get validated yes/no input from user.
    
    Args:
        prompt (str): Input prompt
        
    Returns:
        bool: True for yes, False for no
    """
    valid_yes = ['y']
    valid_no = ['n']
    
    while True:
        try:
            user_input = input(f"{prompt}: ").strip().lower()
            
            if user_input in valid_yes:
                return True
            elif user_input in valid_no:
                return False
            else:
                print("[X] Invalid input! Please enter:")
                print("   - For YES: y")
                print("   - For NO: n")
                continue

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return False


def main():
    """Main application function."""
    try:
                
        # Initialize system manager
        print("\nInitializing Portal System...")
        system_manager = SystemManager()
        
        # Initialize menu manager
        menu_manager = MenuManager(system_manager)
        
        print("System initialized successfully!")
        input("Press Enter to start...")
        
        # Start the main menu loop
        try:
            menu_manager.show_main_menu()
        except KeyboardInterrupt:
            print("\n\nSystem interrupted by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")
        
        # Save data before exit
        print("\nSaving system data...")
        system_manager.save_all_data()
        
        # Create backup
        backup_choice = get_yes_no_input("Would you like to create a backup before exit? (y/n)")
        if backup_choice:
            print("Creating system backup...")
            if system_manager.backup_system():
                print("Backup created successfully!")
            else:
                print("Backup creation failed.")
        
        print("\nThank you for using Portal System!")
        print("System shutdown complete.")
        
    except KeyboardInterrupt:
        print("\n\nSystem interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical error occurred: {e}")
        print("Please check your system configuration and try again.")
        sys.exit(1)


def check_dependencies(verbose=False):
    """Check if required dependencies are available."""
    if verbose:
        print("Checking system dependencies...")
    
    missing_deps = []
    
    try:
        import json
        if verbose:
            print("[√] json module available")
    except ImportError:
        missing_deps.append("json (built-in)")
    
    try:
        import os
        if verbose:
            print("[√] os module available")
    except ImportError:
        missing_deps.append("os (built-in)")
    
    try:
        import datetime
        if verbose:
            print("[√] datetime module available")
    except ImportError:
        missing_deps.append("datetime (built-in)")
    
    try:
        import matplotlib
        if verbose:
            print("[√] matplotlib available")
    except ImportError:
        if verbose:
            print("[!] matplotlib not available (CGPA graphs will not work)")
            print("  Install with: pip install matplotlib")
    
    if missing_deps:
        print(f"\n[X] Missing critical dependencies: {', '.join(missing_deps)}")
        print("Please install missing dependencies and try again.")
        return False
    
    if verbose:
        print("[√] All critical dependencies satisfied")
    return True


def setup_data_directory(verbose=False):
    """Ensure data directory exists."""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            if verbose:
                print(f"[√] Created data directory: {data_dir}")
        except Exception as e:
            print(f"[X] Failed to create data directory: {e}")
            return False
    elif verbose:
        print(f"[√] Data directory exists: {data_dir}")
    
    return True


def run_system_diagnostics(verbose=False):
    """Run basic system diagnostics."""
    if verbose:
        print("\n" + "="*50)
        print("           SYSTEM DIAGNOSTICS")
        print("="*50)
    
    # Check Python version
    python_version = sys.version_info
    if verbose:
        print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        if verbose:
            print("[!] Warning: Python 3.7+ recommended for optimal performance")
    elif verbose:
        print("[√] Python version compatible")
    
    # Check dependencies
    if not check_dependencies(verbose):
        return False
    
    # Setup data directory
    if not setup_data_directory(verbose):
        return False
    
    if verbose:
        print("\n[√] All system checks passed")
        print("="*50)
    return True


if __name__ == "__main__":
    """Application entry point."""
    
    # Run diagnostics silently (no verbose output)
    if not run_system_diagnostics(verbose=False):
        print("System diagnostics failed. Please resolve issues and try again.")
        sys.exit(1)
    
    # Start main application
    main()
