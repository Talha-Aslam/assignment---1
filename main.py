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
    valid_yes = ['y', 'yes', 'yeah', 'yep', 'true', '1']
    valid_no = ['n', 'no', 'nope', 'false', '0']
    
    while True:
        try:
            user_input = input(f"{prompt}: ").strip().lower()
            
            if user_input in valid_yes:
                return True
            elif user_input in valid_no:
                return False
            else:
                print("❌ Invalid input! Please enter:")
                print("   • For YES: y, yes, yeah, yep, true, 1")
                print("   • For NO: n, no, nope, false, 0")
                continue
                
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return False


def display_welcome_message():
    """Display welcome message and system information."""
    print("\n" + "="*80)
    print("                    WELCOME TO PORTAL SYSTEM")
    print("                  Console-Based Education Portal")
    print("="*80)
    print("                    Developed using Python OOP")
    print("                   Supports Students, Teachers & Admins")
    print("="*80)
    print(f"                    System Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)


def display_system_info():
    """Display system information and features."""
    print("\n" + "="*60)
    print("                    SYSTEM FEATURES")
    print("="*60)
    print("STUDENT FEATURES:")
    print("• Course enrollment and unenrollment")
    print("• Academic records and CGPA tracking")
    print("• CGPA trend visualization (matplotlib)")
    print("• Teacher profile viewing")
    print("• Password management")
    print()
    print("TEACHER FEATURES:")
    print("• Profile management with continuous editing")
    print("• Salary slip viewing")
    print("• Personal information updates with cancel options")
    print("• Course assignments")
    print("• Contact management with safe removal")
    print("• Password management")
    print()
    print("ADMIN FEATURES:")
    print("• User creation and management")
    print("• System-wide data access")
    print("• Enrollment management")
    print("• System statistics and logs")
    print("• Auto-generated user credentials")
    print("="*60)


def display_default_credentials():
    """Display default login credentials."""
    print("\n" + "="*60)
    print("                DEFAULT LOGIN CREDENTIALS")
    print("="*60)
    print("ADMIN ACCESS:")
    print("  Username: admin")
    print("  Password: admin123")
    print()
    print("STUDENT ACCESS (Examples):")
    print("  Username: student1, student2, ..., student15")
    print("  Password: pass123 (for all students)")
    print()
    print("TEACHER ACCESS (Examples):")
    print("  Username: teacher1, teacher2, ..., teacher15")
    print("  Password: teach123 (for all teachers)")
    print("="*60)


def main():
    """Main application function."""
    try:
        # Display welcome information
        display_welcome_message()
        
        # Ask if user wants to see system info
        show_info = get_yes_no_input("\nWould you like to see system features and default credentials? (y/n)")
        if show_info:
            display_system_info()
            display_default_credentials()
            input("\nPress Enter to continue to login...")
        
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


def check_dependencies():
    """Check if required dependencies are available."""
    print("Checking system dependencies...")
    
    missing_deps = []
    
    try:
        import json
        print("✓ json module available")
    except ImportError:
        missing_deps.append("json (built-in)")
    
    try:
        import os
        print("✓ os module available")
    except ImportError:
        missing_deps.append("os (built-in)")
    
    try:
        import datetime
        print("✓ datetime module available")
    except ImportError:
        missing_deps.append("datetime (built-in)")
    
    try:
        import matplotlib
        print("✓ matplotlib available")
    except ImportError:
        print("⚠ matplotlib not available (CGPA graphs will not work)")
        print("  Install with: pip install matplotlib")
    
    if missing_deps:
        print(f"\n❌ Missing critical dependencies: {', '.join(missing_deps)}")
        print("Please install missing dependencies and try again.")
        return False
    
    print("✓ All critical dependencies satisfied")
    return True


def setup_data_directory():
    """Ensure data directory exists."""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(f"✓ Created data directory: {data_dir}")
        except Exception as e:
            print(f"❌ Failed to create data directory: {e}")
            return False
    else:
        print(f"✓ Data directory exists: {data_dir}")
    
    return True


def run_system_diagnostics():
    """Run basic system diagnostics."""
    print("\n" + "="*50)
    print("           SYSTEM DIAGNOSTICS")
    print("="*50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("⚠ Warning: Python 3.7+ recommended for optimal performance")
    else:
        print("✓ Python version compatible")
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Setup data directory
    if not setup_data_directory():
        return False
    
    print("\n✓ All system checks passed")
    print("="*50)
    return True


if __name__ == "__main__":
    """Application entry point."""
    print("Starting Portal System...")
    
    # Run diagnostics first
    if not run_system_diagnostics():
        print("System diagnostics failed. Please resolve issues and try again.")
        sys.exit(1)
    
    # Start main application
    main()
