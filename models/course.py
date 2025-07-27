"""
Course class for managing course information and enrollments
"""

import json
from datetime import datetime


class Course:
    """
    Represents a course in the portal system.
    Manages course information, enrollment, and capacity.
    """
    
    def __init__(self, course_id, course_name, instructor, capacity=30, section="A"):
        """
        Initialize a Course object.
        
        Args:
            course_id (str): Unique course identifier
            course_name (str): Name of the course
            instructor (str): Instructor name/ID
            capacity (int): Maximum number of students (default: 30)
            section (str): Course section (default: "A")
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.capacity = capacity
        self.section = section
        self.enrolled_students = []  # List of student IDs
        self.created_date = datetime.now()
    
    def add_student(self, student_id):
        """
        Add a student to the course.
        
        Args:
            student_id (str): Student ID to add
            
        Returns:
            bool: True if student added successfully, False if course is full
        """
        if self.is_full():
            print(f"Course {self.course_name} (Section {self.section}) is full!")
            return False
        
        if student_id in self.enrolled_students:
            print(f"Student {student_id} is already enrolled in this course.")
            return False
        
        self.enrolled_students.append(student_id)
        print(f"Student {student_id} successfully enrolled in {self.course_name}")
        return True
    
    def remove_student(self, student_id):
        """
        Remove a student from the course.
        
        Args:
            student_id (str): Student ID to remove
            
        Returns:
            bool: True if student removed successfully, False if not found
        """
        if student_id in self.enrolled_students:
            self.enrolled_students.remove(student_id)
            print(f"Student {student_id} unenrolled from {self.course_name}")
            return True
        else:
            print(f"Student {student_id} is not enrolled in this course.")
            return False
    
    def is_full(self):
        """
        Check if the course has reached capacity.
        
        Returns:
            bool: True if course is full, False otherwise
        """
        return len(self.enrolled_students) >= self.capacity
    
    def get_available_spots(self):
        """
        Get number of available spots in the course.
        
        Returns:
            int: Number of available spots
        """
        return self.capacity - len(self.enrolled_students)
    
    def get_enrollment_count(self):
        """
        Get current enrollment count.
        
        Returns:
            int: Number of enrolled students
        """
        return len(self.enrolled_students)
    
    def is_student_enrolled(self, student_id):
        """
        Check if a specific student is enrolled.
        
        Args:
            student_id (str): Student ID to check
            
        Returns:
            bool: True if student is enrolled, False otherwise
        """
        return student_id in self.enrolled_students
    
    def get_info(self):
        """
        Get course information as a formatted string.
        
        Returns:
            str: Formatted course information
        """
        return f"""
Course Information:
------------------
Course ID: {self.course_id}
Course Name: {self.course_name}
Section: {self.section}
Instructor: {self.instructor}
Capacity: {self.capacity}
Enrolled: {len(self.enrolled_students)}
Available Spots: {self.get_available_spots()}
Status: {'FULL' if self.is_full() else 'OPEN'}
"""
    
    def get_enrolled_students_list(self):
        """
        Get list of enrolled students.
        
        Returns:
            list: List of student IDs
        """
        return self.enrolled_students.copy()
    
    def to_dict(self):
        """
        Convert course object to dictionary for serialization.
        
        Returns:
            dict: Course data as dictionary
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor,
            'capacity': self.capacity,
            'section': self.section,
            'enrolled_students': self.enrolled_students,
            'created_date': self.created_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create course object from dictionary.
        
        Args:
            data (dict): Course data dictionary
            
        Returns:
            Course: Course object
        """
        course = cls(
            data['course_id'],
            data['course_name'],
            data['instructor'],
            data.get('capacity', 30),
            data.get('section', 'A')
        )
        course.enrolled_students = data.get('enrolled_students', [])
        if 'created_date' in data:
            course.created_date = datetime.fromisoformat(data['created_date'])
        
        return course
    
    def __str__(self):
        """String representation of course."""
        return f"{self.course_name} ({self.course_id}) - Section {self.section}"
    
    def __repr__(self):
        """Official string representation of course."""
        return f"Course(course_id='{self.course_id}', course_name='{self.course_name}', section='{self.section}')"
    
    def __eq__(self, other):
        """Check equality based on course_id and section."""
        if isinstance(other, Course):
            return self.course_id == other.course_id and self.section == other.section
        return False
    
    def __hash__(self):
        """Hash method for using Course objects in sets/dicts."""
        return hash((self.course_id, self.section))
