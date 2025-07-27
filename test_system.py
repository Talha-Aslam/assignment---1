#!/usr/bin/env python3
"""Test script to verify system functionality after section implementation."""

import sys
from system_manager import SystemManager

def test_system():
    """Test system functionality."""
    try:
        print("Creating System Manager...")
        manager = SystemManager()
        print("✅ System Manager created successfully")
        
        # Test course loading
        courses = manager.get_all_courses()
        print(f"✅ Loaded {len(courses)} courses")
        
        # Test section lookup
        print("\n📚 Course Sections:")
        for course in courses[:3]:
            print(f"  {course.course_name} ({course.course_id}) - Section {course.section}")
            print(f"    Key: {course.course_id}-{course.section}")
            print(f"    Enrolled: {len(course.enrolled_students)}/{course.capacity}")
        
        # Check available students
        students = manager.get_all_students()
        print(f"\n👥 Available students: {len(students)}")
        for student in students[:3]:
            print(f"  {student.student_id}: {student.name}")
        
        # Test enrollment with first available student
        course_id = 'CS101'
        section = 'A'
        if students:
            test_student_id = students[0].student_id
            student = students[0]
        else:
            test_student_id = 'S001'
            student = manager.get_user_by_id(test_student_id)
        
        print(f"\n🎓 Testing enrollment for student {test_student_id} in {course_id} section {section}")
        if student:
            print(f"✅ Student found: {student.name}")
            result = manager.enroll_student_in_course(test_student_id, course_id, section)
            print(f"📝 Enrollment result: {result}")
            
            # Test finding enrolled section
            enrolled_section = manager.find_student_enrolled_section(test_student_id, course_id)
            if enrolled_section:
                print(f"✅ Student is enrolled in section: {enrolled_section}")
            else:
                print("❌ Could not find enrolled section")
        else:
            print("❌ Student not found")
            
        print("\n🔍 Testing unenrollment...")
        if student:
            unenroll_result = manager.unenroll_student_from_course(test_student_id, course_id)
            print(f"📝 Unenrollment result: {unenroll_result}")
            
        print("\n✅ System test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_system()
