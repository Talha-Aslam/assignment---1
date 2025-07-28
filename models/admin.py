"""
Admin class extending User base class
Implements administrator-specific functionality
"""

from models.user import User
import json
import random
import string
from datetime import datetime


class SystemLog:
    """Represents a system log entry."""
    
    def __init__(self, log_id, user_id, action, details, timestamp=None):
        self.log_id = log_id
        self.user_id = user_id
        self.action = action
        self.details = details
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        log = cls(
            data['log_id'],
            data['user_id'],
            data['action'],
            data['details']
        )
        log.timestamp = datetime.fromisoformat(data['timestamp'])
        return log


class Admin(User):
    """
    Admin class inheriting from User.
    Implements administrator-specific functionality for system management,
    user creation, and monitoring.
    """
    
    def __init__(self, username, password, name, email, user_id, admin_id=None, access_level="full", first_login=False):
        """
        Initialize an Admin object.
        
        Args:
            username (str): Unique username for login
            password (str): User password
            name (str): Full name of the admin
            email (str): Email address
            user_id (str): Unique user identifier
            admin_id (str): Unique admin identifier
            access_level (str): Admin access level
            first_login (bool): Flag indicating if this is the user's first login
        """
        super().__init__(username, password, name, email, user_id, first_login)
        self.admin_id = admin_id or user_id
        self.access_level = access_level
        self.system_logs = []
        self.created_users = []  # Track users created by this admin
    
    def generate_user_id(self, user_type):
        """
        Generate auto ID for new users.
        
        Args:
            user_type (str): Type of user ('student', 'teacher', 'admin')
            
        Returns:
            str: Generated user ID
        """
        prefix = user_type[:3].upper()
        timestamp = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"{prefix}{timestamp}{random_suffix}"
    
    def generate_password(self, length=8):
        """
        Generate random password for new users.
        
        Args:
            length (int): Password length
            
        Returns:
            str: Generated password
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
    
    def create_user(self, user_type, name, email, custom_username=None, custom_password=None, **kwargs):
        """
        Create a new user with either admin-provided or system-generated username and password.
        
        Args:
            user_type (str): Type of user to create
            name (str): User's full name
            email (str): User's email
            custom_username (str, optional): Admin-provided username (if not provided, one will be generated)
            custom_password (str, optional): Admin-provided password (if not provided, one will be generated)
            **kwargs: Additional user-specific parameters
            
        Returns:
            dict: User credentials and information
        """
        user_id = self.generate_user_id(user_type)
        
        # Use custom username if provided, otherwise generate one
        if custom_username:
            username = custom_username
        else:
            username = f"{user_type.lower()}{user_id[-6:]}"  # Last 6 chars of ID
        
        # Use custom password if provided, otherwise generate one
        if custom_password:
            password = custom_password
        else:
            password = self.generate_password()
        
        # Hash the password for storage
        hashed_password = self._hash_password(password)
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'password': hashed_password,  # Store hashed password
            'plain_password': password,   # Keep plain password for display only
            'name': name,
            'email': email,
            'user_type': user_type,
            'created_by': self.admin_id,
            'created_date': datetime.now().isoformat(),
            'first_login': True           # Flag to indicate this is a new user's first login
        }
        
        # Add user-specific data
        if user_type.lower() == 'student':
            user_data['student_id'] = user_id
            user_data['enrolled_courses'] = []  # Initialize empty list for enrolled courses
        elif user_type.lower() == 'teacher':
            user_data['teacher_id'] = user_id
            user_data['department'] = kwargs.get('department', '')
            user_data['salary'] = kwargs.get('salary', 0.0)
            user_data['courses_teaching'] = []  # Initialize empty list for taught courses
        elif user_type.lower() == 'admin':
            user_data['admin_id'] = user_id
            user_data['access_level'] = kwargs.get('access_level', 'limited')
        
        # Remove plain_password before adding to created_users to avoid storing plain passwords
        user_data_for_storage = user_data.copy()
        if 'plain_password' in user_data_for_storage:
            del user_data_for_storage['plain_password']
        
        self.created_users.append(user_data_for_storage)
        
        # Log the action
        self.log_action(
            f"create_user_{user_type}",
            f"Created {user_type} account for {name} (ID: {user_id})"
        )
        
        # Return the user data with plain password for display in menu
        return user_data
    
    def delete_user(self, username, user_manager):
        """
        Delete a user from the system.
        
        Args:
            username (str): Username of the user to delete
            user_manager: User manager object
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        if user_manager.delete_user_by_username(username):
            self.log_action("delete_user", f"Deleted user account: {username}")
            return True
        else:
            return False
    
    def view_all_data(self, data_manager):
        """
        View all system data.
        
        Args:
            data_manager: Data manager object
        """
        print(f"\n=== System Data Overview ===")
        print(f"Requested by Admin: {self.name} ({self.admin_id})")
        print("-" * 50)
        
        # Get all data from data manager
        all_users = data_manager.get_all_users()
        all_courses = data_manager.get_all_courses()
        
        print(f"Total Users: {len(all_users)}")
        print(f"Total Courses: {len(all_courses)}")
        
        # User breakdown
        user_types = {}
        for user in all_users:
            user_type = user.get('user_type', 'Unknown')
            user_types[user_type] = user_types.get(user_type, 0) + 1
        
        print("\nUser Distribution:")
        for user_type, count in user_types.items():
            print(f"  {user_type}s: {count}")
    
    def manage_enrollments(self, course_manager):
        """
        Manage course enrollments.
        
        Args:
            course_manager: Course manager object
        """
        print(f"\n=== Enrollment Management ===")
        courses = course_manager.get_all_courses()
        
        for course in courses:
            print(f"\nCourse: {course.course_name} ({course.course_id})")
            print(f"Enrolled: {course.get_enrollment_count()}/{course.capacity}")
            print(f"Available: {course.get_available_spots()}")
            if course.enrolled_students:
                print(f"Students: {', '.join(course.enrolled_students[:5])}")
                if len(course.enrolled_students) > 5:
                    print(f"  ... and {len(course.enrolled_students) - 5} more")
    
    def view_statistics(self, data_manager):
        """
        View system statistics.
        
        Args:
            data_manager: Data manager object
        """
        print(f"\n=== System Statistics ===")
        print(f"Generated by: {self.name}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # Basic statistics
        all_users = data_manager.get_all_users()
        all_courses = data_manager.get_all_courses()
        
        total_users = len(all_users)
        total_courses = len(all_courses)
        total_enrollments = sum(len(course.enrolled_students) for course in all_courses)
        
        print(f"Total Users: {total_users}")
        print(f"Total Courses: {total_courses}")
        print(f"Total Enrollments: {total_enrollments}")
        
        if total_courses > 0:
            avg_enrollment = total_enrollments / total_courses
            print(f"Average Enrollment per Course: {avg_enrollment:.2f}")
        
        # User activity (last login)
        recent_logins = sum(1 for user in all_users 
                          if user.get('last_login') and 
                          datetime.fromisoformat(user['last_login']).date() == datetime.now().date())
        print(f"Active Users Today: {recent_logins}")
        
        # System logs count
        print(f"Total System Logs: {len(self.system_logs)}")
        
        # Users created by admins
        admin_created = len(self.created_users)
        print(f"Users Created by This Admin: {admin_created}")
    
    def log_action(self, action, details):
        """
        Log an admin action.
        
        Args:
            action (str): Action performed
            details (str): Action details
        """
        log_id = f"LOG{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
        log_entry = SystemLog(log_id, self.admin_id, action, details)
        self.system_logs.append(log_entry)
    
    def view_logs(self, filter_action=None, filter_date=None):
        """
        View system logs.
        
        Args:
            filter_action (str): Filter by action type
            filter_date (str): Filter by date (YYYY-MM-DD)
        """
        print(f"\n=== System Logs ===")
        print(f"Admin: {self.name}")
        print("-" * 50)
        
        filtered_logs = self.system_logs
        
        if filter_action:
            filtered_logs = [log for log in filtered_logs if filter_action in log.action]
        
        if filter_date:
            filtered_logs = [log for log in filtered_logs 
                           if log.timestamp.strftime('%Y-%m-%d') == filter_date]
        
        if not filtered_logs:
            print("No logs found matching the criteria.")
            return
        
        for log in sorted(filtered_logs, key=lambda x: x.timestamp, reverse=True):
            print(f"[{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {log.action}")
            print(f"  User: {log.user_id}")
            print(f"  Details: {log.details}")
            print("-" * 30)
    
    def display_menu(self):
        """Display admin-specific menu."""
        print(f"\n=== Admin Menu - {self.name} ===")
        print("1. Create New User")
        print("2. Delete User")
        print("3. View All System Data")
        print("4. Manage Enrollments")
        print("5. View System Statistics")
        print("6. View System Logs")
        print("7. Change Password")
        print("8. Export Users Data")
        print("9. Logout")
        print("-" * 30)
    
    def get_user_type(self):
        """Return user type."""
        return "Admin"
    
    def export_users_data(self, all_users, file_path=None):
        """
        Export all users' data to a file.
        
        Args:
            all_users (list): List of user dictionaries
            file_path (str, optional): Path to save the file, if None, uses a default path
            
        Returns:
            tuple: (bool, str) Success status and file path or error message
        """
        import os
        import csv
        import datetime
        
        try:
            # Create export directory if it doesn't exist
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exports')
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate default filename with timestamp if not provided
            if not file_path:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_path = os.path.join(export_dir, f"users_export_{timestamp}.csv")
            
            # Define fields to export (excluding sensitive info like hashed password)
            fields = ['user_id', 'username', 'name', 'email', 'user_type', 'created_date']
            
            # Add user-type specific fields
            student_fields = fields + ['student_id', 'enrolled_courses']
            teacher_fields = fields + ['teacher_id', 'department', 'salary']
            admin_fields = fields + ['admin_id', 'access_level']
            
            # Write to CSV file
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['User ID', 'Username', 'Name', 'Email', 'User Type', 
                                'Creation Date', 'Role-specific ID', 'Additional Info'])
                
                # Write user data
                for user in all_users:
                    user_type = user.get('user_type', '')
                    row = [
                        user.get('user_id', ''),
                        user.get('username', ''),
                        user.get('name', ''),
                        user.get('email', ''),
                        user_type,
                        user.get('created_date', ''),
                    ]
                    
                    # Add role-specific data
                    if user_type.lower() == 'student':
                        row.append(user.get('student_id', ''))
                        row.append(f"Enrolled in {len(user.get('enrolled_courses', []))} courses")
                    elif user_type.lower() == 'teacher':
                        row.append(user.get('teacher_id', ''))
                        row.append(f"Dept: {user.get('department', '')}, Salary: {user.get('salary', '')}")
                    elif user_type.lower() == 'admin':
                        row.append(user.get('admin_id', ''))
                        row.append(f"Access: {user.get('access_level', '')}")
                    
                    writer.writerow(row)
            
            # Log the action
            self.log_action("export_users", f"Exported users data to {file_path}")
            
            return True, file_path
            
        except Exception as e:
            error_msg = f"Failed to export users data: {str(e)}"
            self.log_action("export_users_error", error_msg)
            return False, error_msg
    
    def to_dict(self):
        """Convert admin object to dictionary."""
        data = super().to_dict()
        data.update({
            'admin_id': self.admin_id,
            'access_level': self.access_level,
            'system_logs': [log.to_dict() for log in self.system_logs],
            'created_users': self.created_users
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create admin object from dictionary."""
        admin = cls(
            data['username'],
            '',  # Password is already hashed in data
            data['name'],
            data['email'],
            data['user_id'],
            data.get('admin_id'),
            data.get('access_level', 'full'),
            data.get('first_login', False)  # Add first_login flag
        )
        admin._password = data['password']  # Use hashed password
        admin.created_users = data.get('created_users', [])
        
        # Load system logs
        admin.system_logs = [SystemLog.from_dict(log_data) 
                           for log_data in data.get('system_logs', [])]
        
        return admin
    
    def __str__(self):
        """String representation of admin."""
        return f"Admin: {self.name} (ID: {self.admin_id}) - Access: {self.access_level}"
