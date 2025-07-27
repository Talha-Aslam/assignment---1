"""
Fix users that were created by admin but not properly added to the system.

This script checks for users in admin's created_users list that are not in the main users list
and adds them properly to the system.
"""
import os
import sys
import json
from system_manager import SystemManager

def fix_missing_users():
    """Fix users that were created by admin but not properly added to the system."""
    print("Fixing Missing Users")
    print("====================")
    
    # Initialize system manager
    system_manager = SystemManager()
    
    # Get the admin user
    admin = None
    for user in system_manager.users.values():
        if user.get_user_type().lower() == 'admin':
            admin = user
            break
    
    if not admin:
        print("Error: Admin user not found!")
        return
    
    print(f"Found admin: {admin.name} ({admin.username})")
    
    # Check for users in admin's created_users list that are not in the main system
    created_users = admin.created_users
    missing_users = []
    
    print(f"\nAdmin has {len(created_users)} users in created_users list")
    
    for user_data in created_users:
        username = user_data.get('username')
        if username not in system_manager.users:
            missing_users.append(user_data)
    
    print(f"Found {len(missing_users)} users that were not properly added to the system")
    
    if not missing_users:
        print("\nNo missing users to fix!")
        return
    
    # Add the missing users to the system
    print("\nAdding missing users to system...")
    for user_data in missing_users:
        print(f"Processing {user_data['username']} ({user_data['user_type']})...")
        
        # Save user to system
        result = system_manager.save_user(user_data)
        print(f"  Result: {'Success' if result else 'Failed'}")
    
    print("\nAll missing users have been processed!")
    
    # Verify all users are now in the system
    system_manager = SystemManager()  # Reload the system manager to verify changes
    
    for user_data in created_users:
        username = user_data.get('username')
        if username not in system_manager.users:
            print(f"Warning: {username} is still missing from the system!")
        
    print("\nUser fix completed!")

if __name__ == "__main__":
    fix_missing_users()
