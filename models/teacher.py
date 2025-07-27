"""
Teacher class extending User base class
Implements teacher-specific functionality
"""

from models.user import User
import json
from datetime import datetime


class Teacher(User):
    """
    Teacher class inheriting from User.
    Implements teacher-specific functionality for profile management,
    salary information, and course instruction.
    """
    
    def __init__(self, username, password, name, email, user_id, teacher_id=None, 
                 department="", qualification="", contact_info=None, salary=0.0):
        """
        Initialize a Teacher object.
        
        Args:
            username (str): Unique username for login
            password (str): User password
            name (str): Full name of the teacher
            email (str): Email address
            user_id (str): Unique user identifier
            teacher_id (str): Unique teacher identifier
            department (str): Department/faculty
            qualification (str): Educational qualifications
            contact_info (dict): Contact information
            salary (float): Base salary
        """
        super().__init__(username, password, name, email, user_id)
        self.teacher_id = teacher_id or user_id
        self.department = department
        self.qualification = qualification
        self.contact_info = contact_info or {}
        self.salary = salary
        self.courses_taught = []  # List of course IDs
        self.salary_slips = []  # List of salary slip objects
        self.profile_updates = []  # Track profile changes
        
    def update_info(self, field, value):
        """
        Update teacher information.
        
        Args:
            field (str): Field to update
            value: New value for the field
            
        Returns:
            bool: True if update successful, False otherwise
        """
        valid_fields = ['name', 'department', 'qualification', 'contact_info', 'email']
        
        if field not in valid_fields:
            print(f"Invalid field: {field}")
            return False
        
        old_value = getattr(self, field)
        
        try:
            if field == 'name':
                self.name = value
            elif field == 'email':
                self.email = value
            elif field == 'department':
                self.department = value
            elif field == 'qualification':
                self.qualification = value
            elif field == 'contact_info':
                if isinstance(value, dict):
                    self.contact_info.update(value)
                else:
                    print("Contact info must be a dictionary")
                    return False
            
            # Log the update
            self.profile_updates.append({
                'field': field,
                'old_value': old_value,
                'new_value': value,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"Successfully updated {field}")
            return True
            
        except ValueError as e:
            print(f"Error updating {field}: {e}")
            return False
    
    def add_salary_slip(self, salary_slip):
        """
        Add a salary slip.
        
        Args:
            salary_slip: SalarySlip object
        """
        self.salary_slips.append(salary_slip)
    
    def view_salary(self, month=None):
        """
        View salary slips.
        
        Args:
            month (str): Specific month to view (optional)
        """
        print(f"\n=== Salary Information for {self.name} ===")
        print(f"Teacher ID: {self.teacher_id}")
        print(f"Base Salary: ${self.salary:,.2f}")
        print("-" * 50)
        
        if not self.salary_slips:
            print("No salary slips available.")
            return
        
        for slip in self.salary_slips:
            if month is None or slip.month == month:
                slip.display()
                print("-" * 30)
    
    def view_profile(self):
        """Display teacher profile information."""
        print(f"\n=== Teacher Profile ===")
        print(f"Name: {self.name}")
        print(f"Teacher ID: {self.teacher_id}")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Department: {self.department}")
        print(f"Qualification: {self.qualification}")
        print(f"Base Salary: ${self.salary:,.2f}")
        
        if self.contact_info:
            print("\nContact Information:")
            for key, value in self.contact_info.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        if self.courses_taught:
            print(f"\nCourses Taught: {', '.join(self.courses_taught)}")
        
        print(f"Last Login: {self.last_login}")
    
    def view_public_profile(self):
        """Display public teacher profile information (for students)."""
        print(f"\n=== Teacher Profile ===")
        print(f"Name: {self.name}")
        print(f"Teacher ID: {self.teacher_id}")
        print(f"Email: {self.email}")
        print(f"Department: {self.department}")
        print(f"Qualification: {self.qualification}")
        
        # Only show public contact information (if any)
        if self.contact_info:
            public_contact = {}
            # Only show office-related contact info, not personal
            for key, value in self.contact_info.items():
                if 'office' in key.lower() or 'room' in key.lower():
                    public_contact[key] = value
            
            if public_contact:
                print("\nOffice Contact Information:")
                for key, value in public_contact.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
        
        if self.courses_taught:
            print(f"\nCourses Taught: {', '.join(self.courses_taught)}")
        
        print("\nNote: For detailed information, please contact the teacher directly.")
    
    def add_course(self, course_id):
        """
        Add a course to taught courses list.
        
        Args:
            course_id (str): Course ID to add
        """
        if course_id not in self.courses_taught:
            self.courses_taught.append(course_id)
            print(f"Course {course_id} added to your teaching list.")
        else:
            print(f"Course {course_id} is already in your teaching list.")
    
    def remove_course(self, course_id):
        """
        Remove a course from taught courses list.
        
        Args:
            course_id (str): Course ID to remove
        """
        if course_id in self.courses_taught:
            self.courses_taught.remove(course_id)
            print(f"Course {course_id} removed from your teaching list.")
        else:
            print(f"Course {course_id} is not in your teaching list.")
    
    def get_profile_updates(self):
        """Get list of profile updates."""
        return self.profile_updates.copy()
    
    def get_latest_salary_slip(self):
        """Get the most recent salary slip."""
        if self.salary_slips:
            return max(self.salary_slips, key=lambda slip: slip.month)
        return None
    
    def display_menu(self):
        """Display teacher-specific menu."""
        print(f"\n=== Teacher Menu - {self.name} ===")
        print("1. View Profile")
        print("2. Update Personal Information")
        print("3. View Salary Slips")
        print("4. View Courses Taught")
        print("5. Change Password")
        print("6. Logout")
        print("-" * 30)
    
    def get_user_type(self):
        """Return user type."""
        return "Teacher"
    
    def to_dict(self):
        """Convert teacher object to dictionary."""
        data = super().to_dict()
        data.update({
            'teacher_id': self.teacher_id,
            'department': self.department,
            'qualification': self.qualification,
            'contact_info': self.contact_info,
            'salary': self.salary,
            'courses_taught': self.courses_taught,
            'salary_slips': [slip.to_dict() for slip in self.salary_slips],
            'profile_updates': self.profile_updates
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create teacher object from dictionary."""
        teacher = cls(
            data['username'],
            '',  # Password is already hashed in data
            data['name'],
            data['email'],
            data['user_id'],
            data.get('teacher_id'),
            data.get('department', ''),
            data.get('qualification', ''),
            data.get('contact_info', {}),
            data.get('salary', 0.0)
        )
        teacher._password = data['password']  # Use hashed password
        teacher.courses_taught = data.get('courses_taught', [])
        teacher.profile_updates = data.get('profile_updates', [])
        
        # Load salary slips
        from models.salary_slip import SalarySlip
        teacher.salary_slips = [SalarySlip.from_dict(slip_data) 
                               for slip_data in data.get('salary_slips', [])]
        
        return teacher
    
    def __str__(self):
        """String representation of teacher."""
        return f"Teacher: {self.name} (ID: {self.teacher_id}) - {self.department}"
