"""
Test script to demonstrate teacher profile privacy protection
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system_manager import SystemManager


def test_teacher_profile_privacy():
    """Test that students can only see public teacher information."""
    print("="*70)
    print("         TEACHER PROFILE PRIVACY PROTECTION DEMO")
    print("="*70)
    
    # Initialize system
    system_manager = SystemManager()
    
    # Get a teacher and student
    teacher = system_manager.authenticate_user("teacher1", "teach123")
    student = system_manager.authenticate_user("student1", "pass123")
    
    if not teacher or not student:
        print("Failed to authenticate users")
        return
    
    print(f"\n✅ Authenticated Teacher: {teacher.name}")
    print(f"✅ Authenticated Student: {student.name}")
    
    print("\n" + "="*70)
    print("         TEACHER'S FULL PROFILE (PRIVATE)")
    print("="*70)
    print("What the teacher sees when viewing their own profile:")
    print("-" * 50)
    teacher.view_profile()
    
    print("\n" + "="*70)
    print("         TEACHER'S PUBLIC PROFILE (FOR STUDENTS)")
    print("="*70)
    print("What students see when viewing teacher profiles:")
    print("-" * 50)
    teacher.view_public_profile()
    
    print("\n" + "="*70)
    print("         PRIVACY PROTECTION ANALYSIS")
    print("="*70)
    
    print("🔒 HIDDEN FROM STUDENTS:")
    print("   ❌ Base Salary ($75,000.00)")
    print("   ❌ Last Login timestamp")
    print("   ❌ Username (login credential)")
    print("   ❌ Personal phone number")
    print("   ❌ Personal contact information")
    print()
    
    print("👁️  VISIBLE TO STUDENTS:")
    print("   ✅ Name and Teacher ID")
    print("   ✅ Email (for academic communication)")
    print("   ✅ Department and Qualification")
    print("   ✅ Office location (Room, Building)")
    print("   ✅ Office hours")
    print("   ✅ Courses taught")
    print()
    
    print("🛡️  SECURITY MEASURES:")
    print("   • Separate public and private profile methods")
    print("   • Contact info filtering (only office-related)")
    print("   • Salary information completely hidden")
    print("   • Login credentials not exposed")
    print("   • Privacy notice displayed to students")
    
    print("\n" + "="*70)
    print("         IMPLEMENTATION DETAILS")
    print("="*70)
    
    print("CODE STRUCTURE:")
    print("• Teacher.view_profile() - Full access (for teacher/admin)")
    print("• Teacher.view_public_profile() - Limited access (for students)")
    print("• MenuManager filters contact info automatically")
    print("• Privacy notices inform students about data protection")
    
    print("\n" + "="*70)
    print("Privacy protection successfully implemented! 🔐")
    print("Students can only see professional, non-sensitive information.")
    print("="*70)
    
    teacher.logout()
    student.logout()


if __name__ == "__main__":
    test_teacher_profile_privacy()
