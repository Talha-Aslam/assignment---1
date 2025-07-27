#!/usr/bin/env python3
"""Quick test to verify enrollment/unenrollment workflow."""

from system_manager import SystemManager

def quick_test():
    """Quick test for enrollment functionality."""
    manager = SystemManager()
    
    # Get a student and course
    students = manager.get_all_students()
    student = students[0] if students else None
    
    if not student:
        print("No students found")
        return
    
    # Find a course that has available spots
    available_course = None
    for course_key, course in manager.courses.items():
        if course.get_available_spots() > 0:
            available_course = course
            break
    
    if not available_course:
        print("No courses with available spots")
        return
    
    student_id = student.student_id
    course_id = available_course.course_id
    section = available_course.section
    
    print(f"Testing with student {student_id} ({student.name})")
    print(f"Course: {course_id} Section {section}")
    
    # Check if already enrolled
    enrolled_section = manager.find_student_enrolled_section(student_id, course_id)
    if enrolled_section:
        print(f"Student already enrolled in section: {enrolled_section}")
        # Test unenrollment first
        print("Testing unenrollment...")
        result = manager.unenroll_student_from_course(student_id, course_id)
        print(f"Unenrollment result: {result}")
    
    # Test enrollment
    print("Testing enrollment...")
    result = manager.enroll_student_in_course(student_id, course_id, section)
    print(f"Enrollment result: {result}")
    
    # Verify enrollment
    enrolled_section = manager.find_student_enrolled_section(student_id, course_id)
    if enrolled_section:
        print(f"✅ Verification: Student is now enrolled in {enrolled_section}")
    else:
        print("❌ Verification failed: Student not found in course")

if __name__ == "__main__":
    quick_test()
