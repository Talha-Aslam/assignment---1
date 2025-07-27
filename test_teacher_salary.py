#!/usr/bin/env python3
"""Test current teacher salary display functionality."""

from system_manager import SystemManager

def test_teacher_salary():
    """Test teacher salary viewing functionality."""
    manager = SystemManager()
    
    # Get a teacher
    teachers = manager.get_all_teachers()
    if not teachers:
        print("No teachers found")
        return
    
    teacher = teachers[0]
    print(f"Testing salary view for teacher: {teacher.name} ({teacher.teacher_id})")
    print("="*60)
    
    # Call the view_salary method directly
    teacher.view_salary()

if __name__ == "__main__":
    test_teacher_salary()
