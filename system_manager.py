"""
Main System Manager for the Portal System
Coordinates all components and manages system operations
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

from models.user import User
from models.student import Student
from models.teacher import Teacher
from models.admin import Admin
from models.course import Course
from models.salary_slip import SalarySlip
from utils.file_manager import FileManager
from utils.data_validator import DataValidator


class SystemManager:
    """
    Main system manager that coordinates all portal operations.
    Handles user management, course management, and data persistence.
    """
    
    def __init__(self):
        """Initialize the system manager."""
        self.file_manager = FileManager()
        self.users = {}  # Dictionary of username -> User object
        self.courses = {}  # Dictionary of course_id -> Course object
        self.logged_in_users = {}  # Track currently logged in users
        
        # Load existing data
        self.load_all_data()
        
        # Initialize with default data if empty
        if not self.users:
            self.initialize_default_data()
    
    def load_all_data(self):
        """Load all data from files."""
        print("Loading system data...")
        
        # Load users
        users_data = self.file_manager.load_data('users')
        for user_data in users_data:
            user = self.create_user_from_data(user_data)
            if user:
                self.users[user.username] = user
        
        # Load courses with section-aware keys
        courses_data = self.file_manager.load_data('courses')
        for course_data in courses_data:
            course = Course.from_dict(course_data)
            # Create unique key using course_id + section
            course_key = f"{course.course_id}-{course.section}"
            self.courses[course_key] = course
        
        print(f"Loaded {len(self.users)} users and {len(self.courses)} course sections.")
    
    def save_all_data(self):
        """Save all data to files."""
        print("Saving system data...")
        
        # Save users
        users_data = [user.to_dict() for user in self.users.values()]
        self.file_manager.save_data('users', users_data)
        
        # Save courses
        courses_data = [course.to_dict() for course in self.courses.values()]
        self.file_manager.save_data('courses', courses_data)
        
        print("Data saved successfully.")
    
    def create_user_from_data(self, user_data: Dict[str, Any]) -> Optional[User]:
        """
        Create user object from data dictionary.
        
        Args:
            user_data (dict): User data dictionary
            
        Returns:
            User object or None if creation fails
        """
        try:
            user_type = user_data.get('user_type', '').lower()
            
            if user_type == 'student':
                return Student.from_dict(user_data)
            elif user_type == 'teacher':
                return Teacher.from_dict(user_data)
            elif user_type == 'admin':
                return Admin.from_dict(user_data)
            else:
                print(f"Unknown user type: {user_type}")
                return None
                
        except Exception as e:
            print(f"Error creating user from data: {e}")
            return None
    
    def initialize_default_data(self):
        """Initialize system with default users and courses."""
        print("Initializing default data...")
        
        # Create default admin
        admin = Admin(
            username="admin",
            password="admin123",
            name="System Administrator",
            email="admin@portal.edu",
            user_id="ADM001",
            admin_id="ADM001"
        )
        self.users[admin.username] = admin
        
        # Create default students (10-15)
        for i in range(1, 16):
            student_id = f"STU{i:03d}"
            student = Student(
                username=f"student{i}",
                password="pass123",
                name=f"Student {i}",
                email=f"student{i}@portal.edu",
                user_id=student_id,
                student_id=student_id
            )
            
            # Add some sample academic records
            if i <= 5:  # First 5 students get sample records
                student.add_semester_record(
                    "Fall 2023",
                    {"CS101": "A", "MATH101": "B+", "ENG101": "A-"},
                    3.67
                )
                student.add_semester_record(
                    "Spring 2024",
                    {"CS102": "A-", "MATH102": "A", "PHYS101": "B"},
                    3.78
                )
            
            self.users[student.username] = student
        
        # Create default teachers (10-15)
        departments = ["Computer Science", "Mathematics", "Physics", "English", "Business"]
        office_buildings = ["Science Building", "Math Building", "Physics Lab", "Liberal Arts", "Business Center"]
        
        for i in range(1, 16):
            teacher_id = f"TCH{i:03d}"
            dept_index = (i-1) % len(departments)
            teacher = Teacher(
                username=f"teacher{i}",
                password="teach123",
                name=f"Professor {i}",
                email=f"teacher{i}@portal.edu",
                user_id=teacher_id,
                teacher_id=teacher_id,
                department=departments[dept_index],
                qualification="PhD",
                salary=75000 + (i * 1000),
                contact_info={
                    "office_room": f"Room {100 + i}",
                    "office_building": office_buildings[dept_index],
                    "office_hours": "Mon-Wed 2-4 PM",
                    "personal_phone": f"555-{1000+i:04d}"  # This won't be shown to students
                }
            )
            
            # Add sample salary slip
            salary_slip = SalarySlip(
                slip_id=f"PAY{teacher_id}{datetime.now().strftime('%Y%m')}",
                teacher_id=teacher_id,
                month="January",
                year=2024,
                basic_salary=teacher.salary,
                allowances={"Housing": 10000, "Transport": 5000},
                deductions={"Tax": 8000, "Insurance": 2000}
            )
            teacher.add_salary_slip(salary_slip)
            
            self.users[teacher.username] = teacher
        
        # Create default courses
        courses_data = [
            ("CS101", "Introduction to Programming", "teacher1", 30, "A"),
            ("CS102", "Data Structures", "teacher1", 25, "A"),
            ("MATH101", "Calculus I", "teacher2", 40, "A"),
            ("MATH102", "Calculus II", "teacher2", 35, "A"),
            ("PHYS101", "Physics I", "teacher3", 30, "A"),
            ("ENG101", "English Composition", "teacher4", 25, "A"),
            ("BUS101", "Business Fundamentals", "teacher5", 35, "A"),
        ]
        
        for course_id, name, instructor, capacity, section in courses_data:
            course = Course(course_id, name, instructor, capacity, section)
            self.courses[course_id] = course
        
        # Enroll some students in courses
        enrollment_data = [
            ("student1", ["CS101", "MATH101", "ENG101"]),
            ("student2", ["CS101", "MATH101", "PHYS101"]),
            ("student3", ["CS102", "MATH102", "BUS101"]),
            ("student4", ["CS101", "ENG101", "BUS101"]),
            ("student5", ["MATH101", "PHYS101", "ENG101"]),
        ]
        
        for username, course_ids in enrollment_data:
            if username in self.users:
                student = self.users[username]
                for course_id in course_ids:
                    if course_id in self.courses:
                        course = self.courses[course_id]
                        if course.add_student(student.student_id):
                            student.enrolled_courses.append(course_id)
        
        # Save the initialized data
        self.save_all_data()
        print("Default data initialized successfully.")
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user login.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        if username in self.users:
            user = self.users[username]
            if user.login(username, password):
                self.logged_in_users[username] = user
                return user
        return None
    
    def logout_user(self, username: str) -> bool:
        """
        Logout user.
        
        Args:
            username (str): Username to logout
            
        Returns:
            bool: True if logout successful
        """
        if username in self.logged_in_users:
            user = self.logged_in_users[username]
            user.logout()
            del self.logged_in_users[username]
            self.save_all_data()
            return True
        return False
    
    def get_available_courses(self) -> List[Course]:
        """
        Get list of available courses (not full).
        
        Returns:
            list: List of available Course objects
        """
        return [course for course in self.courses.values() if not course.is_full()]
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses."""
        return list(self.courses.values())
    
    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        """
        Get course by ID. Returns the first available section.
        For backward compatibility with existing enrollment data.
        
        Args:
            course_id (str): Course ID
            
        Returns:
            Course object or None
        """
        # First try direct lookup for backward compatibility
        if course_id in self.courses:
            return self.courses[course_id]
        
        # Then search for course sections
        for course_key, course in self.courses.items():
            if course.course_id == course_id:
                return course
        
        return None
    
    def get_course_by_id_and_section(self, course_id: str, section: str) -> Optional[Course]:
        """
        Get course by ID and section.
        
        Args:
            course_id (str): Course ID
            section (str): Section
            
        Returns:
            Course object or None
        """
        course_key = f"{course_id}-{section}"
        return self.courses.get(course_key)
    
    def get_all_sections_by_course_id(self, course_id: str) -> List[Course]:
        """
        Get all sections for a given course ID.
        
        Args:
            course_id (str): Course ID
            
        Returns:
            List of Course objects for all sections
        """
        sections = []
        for course in self.courses.values():
            if course.course_id == course_id:
                sections.append(course)
        return sections
    
    def find_student_enrolled_section(self, student_id: str, course_id: str) -> Optional[Course]:
        """
        Find which section a student is enrolled in for a given course.
        
        Args:
            student_id (str): Student ID
            course_id (str): Course ID
            
        Returns:
            Course object of the section where student is enrolled, or None
        """
        for course in self.courses.values():
            if course.course_id == course_id and student_id in course.enrolled_students:
                return course
        return None
    
    def enroll_student_in_course(self, student_id: str, course_id: str, section: str = None) -> bool:
        """
        Enroll student in course section.
        
        Args:
            student_id (str): Student ID
            course_id (str): Course ID
            section (str): Section (optional, will find first available if not specified)
            
        Returns:
            bool: True if enrollment successful
        """
        # Find student by student_id
        student = None
        for user in self.users.values():
            if hasattr(user, 'student_id') and user.student_id == student_id:
                student = user
                break
        
        if not student:
            print(f"Student {student_id} not found.")
            return False
        
        # Check if student is already enrolled in any section of this course
        existing_section = self.find_student_enrolled_section(student_id, course_id)
        if existing_section:
            print(f"Student {student_id} is already enrolled in {course_id} Section {existing_section.section}")
            return False
        
        # Find the target course section
        target_course = None
        if section:
            # Specific section requested
            target_course = self.get_course_by_id_and_section(course_id, section)
            if not target_course:
                print(f"Course {course_id} Section {section} not found.")
                return False
        else:
            # Find first available section
            sections = self.get_all_sections_by_course_id(course_id)
            for course_section in sections:
                if not course_section.is_full():
                    target_course = course_section
                    break
            
            if not target_course:
                print(f"No available sections found for course {course_id}")
                return False
        
        # Attempt enrollment
        if target_course.add_student(student_id):
            # Add course_id to student's enrolled courses (base course ID, not section-specific)
            if course_id not in student.enrolled_courses:
                student.enrolled_courses.append(course_id)
            self.save_all_data()
            return True
        
        return False
    
    def unenroll_student_from_course(self, student_id: str, course_id: str) -> bool:
        """
        Unenroll student from course.
        
        Args:
            student_id (str): Student ID
            course_id (str): Course ID
            
        Returns:
            bool: True if unenrollment successful
        """
        # Find student by student_id
        student = None
        for user in self.users.values():
            if hasattr(user, 'student_id') and user.student_id == student_id:
                student = user
                break
        
        if not student:
            print(f"Student {student_id} not found.")
            return False
        
        # Find which section the student is enrolled in
        enrolled_section = self.find_student_enrolled_section(student_id, course_id)
        if not enrolled_section:
            print(f"Student {student_id} is not enrolled in course {course_id}")
            return False
        
        # Remove student from the section
        if enrolled_section.remove_student(student_id):
            # Remove course_id from student's enrolled courses
            if course_id in student.enrolled_courses:
                student.enrolled_courses.remove(course_id)
            self.save_all_data()
            return True
        
        return False
    
    def get_all_teachers(self) -> List[Teacher]:
        """Get all teacher objects."""
        return [user for user in self.users.values() if isinstance(user, Teacher)]
    
    def get_all_students(self) -> List[Student]:
        """Get all student objects."""
        return [user for user in self.users.values() if isinstance(user, Student)]
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by their ID (student_id, teacher_id, admin_id)."""
        for user in self.users.values():
            if hasattr(user, 'student_id') and user.student_id == user_id:
                return user
            elif hasattr(user, 'teacher_id') and user.teacher_id == user_id:
                return user
            elif hasattr(user, 'admin_id') and user.admin_id == user_id:
                return user
        return None
    
    def get_all_admins(self) -> List[Admin]:
        """Get all admin objects."""
        return [user for user in self.users.values() if isinstance(user, Admin)]
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users as dictionaries."""
        return [user.to_dict() for user in self.users.values()]
    
    def save_user(self, user_data: Dict[str, Any]) -> bool:
        """
        Save new user to system.
        
        Args:
            user_data (dict): User data dictionary
            
        Returns:
            bool: True if save successful
        """
        try:
            user = self.create_user_from_data(user_data)
            if user:
                self.users[user.username] = user
                self.save_all_data()
                return True
            return False
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user from system.
        
        Args:
            user_id (str): User ID to delete
            
        Returns:
            bool: True if deletion successful
        """
        try:
            # Find user by user_id
            user_to_delete = None
            username_to_delete = None
            
            for username, user in self.users.items():
                if user.user_id == user_id:
                    user_to_delete = user
                    username_to_delete = username
                    break
            
            if not user_to_delete:
                print(f"User with ID {user_id} not found.")
                return False
            
            # Remove user from system
            del self.users[username_to_delete]
            
            # Remove user from logged in users if present
            if username_to_delete in self.logged_in_users:
                del self.logged_in_users[username_to_delete]
            
            # If student, remove from all course enrollments
            if isinstance(user_to_delete, Student):
                for course in self.courses.values():
                    course.remove_student(user_to_delete.student_id)
            
            self.save_all_data()
            return True
            
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def save_user_data(self):
        """Save current user data."""
        self.save_all_data()
    
    def backup_system(self) -> bool:
        """Create system backup."""
        return self.file_manager.backup_data()
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Get system statistics.
        
        Returns:
            dict: System statistics
        """
        total_users = len(self.users)
        total_students = len(self.get_all_students())
        total_teachers = len(self.get_all_teachers())
        total_admins = len(self.get_all_admins())
        total_courses = len(self.courses)
        total_enrollments = sum(len(course.enrolled_students) for course in self.courses.values())
        
        return {
            'total_users': total_users,
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_admins': total_admins,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'logged_in_users': len(self.logged_in_users),
            'timestamp': datetime.now().isoformat()
        }
