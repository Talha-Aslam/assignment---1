"""
Student class extending User base class
Implements student-specific functionality
"""

from models.user import User
import matplotlib.pyplot as plt
import json
from datetime import datetime


class Student(User):
    """
    Student class inheriting from User.
    Implements student-specific functionality for course enrollment,
    academic records, and CGPA tracking.
    """
    
    def __init__(self, username, password, name, email, user_id, student_id=None):
        """
        Initialize a Student object.
        
        Args:
            username (str): Unique username for login
            password (str): User password
            name (str): Full name of the student
            email (str): Email address
            user_id (str): Unique user identifier
            student_id (str): Unique student identifier
        """
        super().__init__(username, password, name, email, user_id)
        self.student_id = student_id or user_id
        self.enrolled_courses = []  # List of course IDs
        self.academic_records = {}  # Semester-wise records
        self.cgpa_history = []  # List of CGPA per semester
        self.semester_data = {}  # Detailed semester information
    
    def enroll_course(self, course_id, course_manager):
        """
        Enroll in a course.
        
        Args:
            course_id (str): Course ID to enroll in
            course_manager: Course manager object to handle enrollment
            
        Returns:
            bool: True if enrollment successful, False otherwise
        """
        if course_id in self.enrolled_courses:
            print(f"You are already enrolled in course {course_id}")
            return False
        
        # Check with course manager if enrollment is possible
        if course_manager.enroll_student_in_course(self.student_id, course_id):
            self.enrolled_courses.append(course_id)
            print(f"Successfully enrolled in course {course_id}")
            return True
        else:
            print(f"Failed to enroll in course {course_id}")
            return False
    
    def unenroll_course(self, course_id, course_manager):
        """
        Unenroll from a course.
        
        Args:
            course_id (str): Course ID to unenroll from
            course_manager: Course manager object to handle unenrollment
            
        Returns:
            bool: True if unenrollment successful, False otherwise
        """
        if course_id not in self.enrolled_courses:
            print(f"You are not enrolled in course {course_id}")
            return False
        
        if course_manager.unenroll_student_from_course(self.student_id, course_id):
            self.enrolled_courses.remove(course_id)
            print(f"Successfully unenrolled from course {course_id}")
            return True
        else:
            print(f"Failed to unenroll from course {course_id}")
            return False
    
    def add_semester_record(self, semester, courses_grades, cgpa):
        """
        Add academic record for a semester.
        
        Args:
            semester (str): Semester identifier (e.g., "Fall 2023")
            courses_grades (dict): Dictionary of course_id: grade
            cgpa (float): CGPA for the semester
        """
        self.academic_records[semester] = {
            'courses_grades': courses_grades,
            'cgpa': cgpa,
            'date_added': datetime.now().isoformat()
        }
        
        self.cgpa_history.append({
            'semester': semester,
            'cgpa': cgpa,
            'date': datetime.now().isoformat()
        })
        
        self.semester_data[semester] = {
            'total_courses': len(courses_grades),
            'grades': courses_grades,
            'cgpa': cgpa
        }
    
    def view_records(self):
        """Display academic records."""
        print(f"\n=== Academic Records for {self.name} ===")
        print(f"Student ID: {self.student_id}")
        print("-" * 50)
        
        if not self.academic_records:
            print("No academic records found.")
            return
        
        for semester, record in self.academic_records.items():
            print(f"\nSemester: {semester}")
            print(f"CGPA: {record['cgpa']:.2f}")
            print("Courses and Grades:")
            for course, grade in record['courses_grades'].items():
                print(f"  {course}: {grade}")
        
        if self.cgpa_history:
            latest_cgpa = self.cgpa_history[-1]['cgpa']
            print(f"\nCurrent CGPA: {latest_cgpa:.2f}")
    
    def plot_cgpa(self):
        """Plot CGPA trends using matplotlib."""
        if not self.cgpa_history:
            print("No CGPA data available to plot.")
            return
        
        try:
            semesters = [record['semester'] for record in self.cgpa_history]
            cgpas = [record['cgpa'] for record in self.cgpa_history]
            
            plt.figure(figsize=(10, 6))
            plt.plot(semesters, cgpas, marker='o', linewidth=2, markersize=8)
            plt.title(f'CGPA Trend for {self.name} (ID: {self.student_id})', fontsize=14)
            plt.xlabel('Semester', fontsize=12)
            plt.ylabel('CGPA', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.ylim(0, 4.0)  # Assuming 4.0 scale
            
            # Add value labels on points
            for i, (sem, cgpa) in enumerate(zip(semesters, cgpas)):
                plt.annotate(f'{cgpa:.2f}', (sem, cgpa), 
                           textcoords="offset points", xytext=(0,10), ha='center')
            
            plt.tight_layout()
            plt.show()
            
        except ImportError:
            print("Matplotlib not available. Cannot display graph.")
            print("Install matplotlib using: pip install matplotlib")
        except Exception as e:
            print(f"Error creating plot: {e}")
    
    def view_teacher_profile(self, teacher_id, teacher_manager):
        """
        View a teacher's public profile (without sensitive information).
        
        Args:
            teacher_id (str): Teacher ID to view
            teacher_manager: Teacher manager object
        """
        # Find teacher by ID
        teacher = None
        for user in teacher_manager.users.values():
            if hasattr(user, 'teacher_id') and user.teacher_id == teacher_id:
                teacher = user
                break
        
        if teacher:
            teacher.view_public_profile()
        else:
            print(f"Teacher with ID {teacher_id} not found.")
    
    def get_enrolled_courses(self):
        """Get list of enrolled courses."""
        return self.enrolled_courses.copy()
    
    def get_current_cgpa(self):
        """Get current CGPA."""
        if self.cgpa_history:
            return self.cgpa_history[-1]['cgpa']
        return 0.0
    
    def display_menu(self):
        """Display student-specific menu."""
        print(f"\n=== Student Menu - {self.name} ===")
        print("1. Enroll in Course")
        print("2. Unenroll from Course (with confirmation)")
        print("3. View Academic Records")
        print("4. Plot CGPA Graph")
        print("5. View Teacher Profile")
        print("6. View Enrolled Courses")
        print("7. Change Password")
        print("8. Logout")
        print("-" * 30)
    
    def get_user_type(self):
        """Return user type."""
        return "Student"
    
    def to_dict(self):
        """Convert student object to dictionary."""
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'enrolled_courses': self.enrolled_courses,
            'academic_records': self.academic_records,
            'cgpa_history': self.cgpa_history,
            'semester_data': self.semester_data
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create student object from dictionary."""
        student = cls(
            data['username'],
            '',  # Password is already hashed in data
            data['name'],
            data['email'],
            data['user_id'],
            data.get('student_id')
        )
        student._password = data['password']  # Use hashed password
        student.enrolled_courses = data.get('enrolled_courses', [])
        student.academic_records = data.get('academic_records', {})
        student.cgpa_history = data.get('cgpa_history', [])
        student.semester_data = data.get('semester_data', {})
        
        return student
    
    def __str__(self):
        """String representation of student."""
        return f"Student: {self.name} (ID: {self.student_id})"
