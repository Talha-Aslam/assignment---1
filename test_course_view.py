#!/usr/bin/env python3
"""Test the course view fix for sections."""

from system_manager import SystemManager

def test_course_view():
    """Test student course viewing functionality."""
    manager = SystemManager()
    
    # Get a student who is enrolled in Physics Section B
    student_id = "STU001"  # From the JSON, this student is in PHYS101 Section B
    
    print(f"Testing course view for student {student_id}")
    
    # Get enrolled courses using the new logic (same as menu_manager)
    enrolled_courses = []
    for course_key, course in manager.courses.items():
        if student_id in course.enrolled_students:
            enrolled_courses.append(course)
    
    print(f"\nEnrolled courses found: {len(enrolled_courses)}")
    for course in enrolled_courses:
        print(f"- {course.course_name} ({course.course_id}) - Section {course.section}")
        print(f"  Instructor: {course.instructor}")
    
    # Also show what the old method would return
    student = manager.get_user_by_id(student_id)
    if student:
        print(f"\nOld method enrolled courses: {student.get_enrolled_courses()}")
        for course_id in student.get_enrolled_courses():
            course = manager.get_course_by_id(course_id)
            if course:
                print(f"- Old method would show: {course.course_name} Section {course.section}")

if __name__ == "__main__":
    test_course_view()
