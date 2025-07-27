"""
Debug script for user creation functionality.
"""
import os
import sys
import json
from system_manager import SystemManager

def main():
    """Main function to debug user creation."""
    print("Debug User Creation Process")
    print("==========================")
    
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
    
    # Create a test user
    print("\nCreating test user...")
    user_data = admin.create_user("Student", "Test Student", "teststudent@example.com")
    
    # Print the user data
    print("\nUser data created by admin:")
    print(json.dumps(user_data, indent=2, default=str))
    
    # Save the user
    print("\nSaving user to system...")
    result = system_manager.save_user(user_data)
    print(f"Save result: {result}")
    
    # Check if the user exists in the system
    if user_data['username'] in system_manager.users:
        print(f"\nUser {user_data['username']} found in system.users!")
    else:
        print(f"\nError: User {user_data['username']} not found in system.users!")
    
    # Load the users.json file to verify the user was saved
    print("\nChecking users.json file...")
    users_file = os.path.join('data', 'users.json')
    if not os.path.exists(users_file):
        print(f"Error: {users_file} not found!")
        return
        
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    # Look for the test user in the file
    found = False
    for user in users_data:
        if user.get('username') == user_data['username']:
            found = True
            break
    
    if found:
        print(f"User {user_data['username']} found in users.json!")
    else:
        print(f"Error: User {user_data['username']} not found in users.json!")
        
    # Check if user is in admin's created_users list
    admin_in_file = next((u for u in users_data if u.get('username') == 'admin'), None)
    if admin_in_file:
        admin_created_users = admin_in_file.get('created_users', [])
        found_in_admin = any(u.get('username') == user_data['username'] for u in admin_created_users)
        print(f"\nUser found in admin's created_users: {found_in_admin}")
    else:
        print("\nCouldn't find admin in users.json!")

if __name__ == "__main__":
    main()
