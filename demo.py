"""
Demo script to showcase the Portal System functionality
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system_manager import SystemManager
from models.student import Student
from models.teacher import Teacher
from models.admin import Admin


def demo_system():
    """Demonstrate the portal system functionality."""
    print("="*80)
    print("                    PORTAL SYSTEM DEMONSTRATION")
    print("="*80)
    
    # Initialize system
    print("\n1. Initializing System Manager...")
    system_manager = SystemManager()
    print("✓ System initialized successfully!")
    
    # Show system statistics
    print("\n2. System Statistics:")
    stats = system_manager.get_system_statistics()
    for key, value in stats.items():
        if key != 'timestamp':
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Demonstrate user authentication
    print("\n3. User Authentication Demo:")
    
    # Try to authenticate a student
    print("   Authenticating student1...")
    student = system_manager.authenticate_user("student1", "pass123")
    if student:
        print(f"   ✓ Login successful: {student.name} ({student.get_user_type()})")
        print(f"   Student ID: {student.student_id}")
        print(f"   Enrolled Courses: {len(student.enrolled_courses)}")
        student.logout()
    
    # Try to authenticate a teacher
    print("\n   Authenticating teacher1...")
    teacher = system_manager.authenticate_user("teacher1", "teach123")
    if teacher:
        print(f"   ✓ Login successful: {teacher.name} ({teacher.get_user_type()})")
        print(f"   Teacher ID: {teacher.teacher_id}")
        print(f"   Department: {teacher.department}")
        print(f"   Salary: ${teacher.salary:,.2f}")
        teacher.logout()
    
    # Try to authenticate admin
    print("\n   Authenticating admin...")
    admin = system_manager.authenticate_user("admin", "admin123")
    if admin:
        print(f"   ✓ Login successful: {admin.name} ({admin.get_user_type()})")
        print(f"   Admin ID: {admin.admin_id}")
        print(f"   Access Level: {admin.access_level}")
        admin.logout()
    
    # Show available courses
    print("\n4. Available Courses:")
    courses = system_manager.get_available_courses()
    for course in courses[:5]:  # Show first 5 courses
        print(f"   {course.course_id}: {course.course_name}")
        print(f"      Instructor: {course.instructor}")
        print(f"      Capacity: {course.get_enrollment_count()}/{course.capacity}")
        print(f"      Available: {course.get_available_spots()} spots")
        print()
    
    # Demonstrate course enrollment
    print("5. Course Enrollment Demo:")
    student = system_manager.authenticate_user("student10", "pass123")
    if student:
        print(f"   Student {student.name} currently enrolled in: {len(student.enrolled_courses)} courses")
        
        # Try to enroll in a new course
        available_courses = system_manager.get_available_courses()
        if available_courses:
            course_to_enroll = available_courses[0]
            if course_to_enroll.course_id not in student.enrolled_courses:
                success = system_manager.enroll_student_in_course(
                    student.student_id, course_to_enroll.course_id
                )
                if success:
                    print(f"   ✓ Successfully enrolled in {course_to_enroll.course_name}")
                else:
                    print(f"   ✗ Failed to enroll in {course_to_enroll.course_name}")
        
        student.logout()
    
    # Show academic records demo
    print("\n6. Academic Records Demo:")
    student = system_manager.authenticate_user("student1", "pass123")
    if student and student.academic_records:
        print(f"   Academic records for {student.name}:")
        for semester, record in student.academic_records.items():
            print(f"   {semester}: CGPA {record['cgpa']:.2f}")
            for course, grade in record['courses_grades'].items():
                print(f"      {course}: {grade}")
        student.logout()
    
    # Show teacher salary demo
    print("\n7. Teacher Salary Demo:")
    teacher = system_manager.authenticate_user("teacher1", "teach123")
    if teacher and teacher.salary_slips:
        print(f"   Salary information for {teacher.name}:")
        latest_slip = teacher.get_latest_salary_slip()
        if latest_slip:
            print(f"   Latest Salary Slip ({latest_slip.month} {latest_slip.year}):")
            print(f"      Basic Salary: ${latest_slip.basic_salary:,.2f}")
            print(f"      Total Allowances: ${sum(latest_slip.allowances.values()):,.2f}")
            print(f"      Total Deductions: ${sum(latest_slip.deductions.values()):,.2f}")
            print(f"      Net Salary: ${latest_slip.net_salary:,.2f}")
        teacher.logout()
    
    # Admin functionality demo
    print("\n8. Admin Functionality Demo:")
    admin = system_manager.authenticate_user("admin", "admin123")
    if admin:
        print(f"   Admin {admin.name} capabilities:")
        print(f"   • Created {len(admin.created_users)} users")
        print(f"   • Logged {len(admin.system_logs)} system actions")
        print(f"   • Can manage all system data")
        print(f"   • Can view system statistics")
        admin.logout()
    
    print("\n" + "="*80)
    print("                    DEMONSTRATION COMPLETE")
    print("="*80)
    print("Key Features Demonstrated:")
    print("✓ Object-Oriented Programming (Inheritance, Encapsulation, Polymorphism)")
    print("✓ User Authentication and Role-based Access")
    print("✓ Course Management and Enrollment")
    print("✓ Academic Records Tracking")
    print("✓ Teacher Profile and Salary Management")
    print("✓ Admin System Management")
    print("✓ Data Persistence and File Management")
    print("="*80)


if __name__ == "__main__":
    demo_system()
