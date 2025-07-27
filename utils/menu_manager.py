"""
Menu Manager utility for handling user interface menus
"""

import os
import sys
from typing import Dict, Any, Callable, Optional


class MenuManager:
    """
    Manages menu systems for different user types in the portal system.
    Provides consistent interface and navigation functionality.
    """
    
    def __init__(self, system_manager):
        """
        Initialize MenuManager.
        
        Args:
            system_manager: Main system manager object
        """
        self.system_manager = system_manager
        self.current_user = None
        self.running = False
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """
        Print formatted header.
        
        Args:
            title (str): Header title
        """
        print("\n" + "="*60)
        print(f"    {title.upper()}")
        print("="*60)
    
    def print_footer(self):
        """Print formatted footer."""
        print("="*60)
    
    def get_user_input(self, prompt: str, input_type: type = str, validator: Optional[Callable] = None) -> Any:
        """
        Get validated user input.
        
        Args:
            prompt (str): Input prompt
            input_type (type): Expected input type
            validator (Callable): Optional validation function
            
        Returns:
            Validated user input
        """
        while True:
            try:
                user_input = input(f"\n{prompt}: ").strip()
                
                if input_type == int:
                    user_input = int(user_input)
                elif input_type == float:
                    user_input = float(user_input)
                
                if validator:
                    if validator(user_input):
                        return user_input
                    else:
                        print("Invalid input. Please try again.")
                        continue
                
                return user_input
                
            except ValueError:
                print(f"Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None
    
    def show_main_menu(self):
        """Display main login menu."""
        while True:
            self.clear_screen()
            self.print_header("Portal System - Main Menu")
            print("1. Student Login")
            print("2. Teacher Login")
            print("3. Admin Login")
            print("4. Exit")
            self.print_footer()
            
            choice = self.get_user_input("Select an option (1-4)", int, 
                                       lambda x: 1 <= x <= 4)
            
            if choice is None:  # Cancelled
                continue
            elif choice == 1:
                self.handle_login("Student")
            elif choice == 2:
                self.handle_login("Teacher")
            elif choice == 3:
                self.handle_login("Admin")
            elif choice == 4:
                print("\nThank you for using Portal System. Goodbye!")
                return False
    
    def handle_login(self, user_type: str):
        """
        Handle user login process.
        
        Args:
            user_type (str): Type of user logging in
        """
        self.clear_screen()
        self.print_header(f"{user_type} Login")
        
        username = self.get_user_input("Username")
        if username is None:
            return
        
        password = self.get_user_input("Password")
        if password is None:
            return
        
        # Attempt login through system manager
        user = self.system_manager.authenticate_user(username, password)
        
        if user and user.get_user_type().lower() == user_type.lower():
            self.current_user = user
            print(f"\nLogin successful! Welcome, {user.name}")
            input("Press Enter to continue...")
            self.show_user_menu()
        else:
            print(f"\nInvalid credentials or incorrect user type.")
            input("Press Enter to continue...")
    
    def show_user_menu(self):
        """Display user-specific menu based on user type."""
        if not self.current_user:
            return
        
        user_type = self.current_user.get_user_type().lower()
        
        if user_type == "student":
            self.show_student_menu()
        elif user_type == "teacher":
            self.show_teacher_menu()
        elif user_type == "admin":
            self.show_admin_menu()
    
    def show_student_menu(self):
        """Display student-specific menu."""
        while self.current_user and self.current_user.is_logged_in:
            self.clear_screen()
            self.current_user.display_menu()
            
            choice = self.get_user_input("Select an option", int,
                                       lambda x: 1 <= x <= 8)
            
            if choice is None:
                continue
            
            if choice == 1:
                self.handle_student_enroll_course()
            elif choice == 2:
                self.handle_student_unenroll_course()
            elif choice == 3:
                self.handle_student_view_records()
            elif choice == 4:
                self.handle_student_plot_cgpa()
            elif choice == 5:
                self.handle_student_view_teacher()
            elif choice == 6:
                self.handle_student_view_courses()
            elif choice == 7:
                self.handle_change_password()
            elif choice == 8:
                self.handle_logout()
                break
    
    def show_teacher_menu(self):
        """Display teacher-specific menu."""
        while self.current_user and self.current_user.is_logged_in:
            self.clear_screen()
            self.current_user.display_menu()
            
            choice = self.get_user_input("Select an option", int,
                                       lambda x: 1 <= x <= 6)
            
            if choice is None:
                continue
            
            if choice == 1:
                self.handle_teacher_view_profile()
            elif choice == 2:
                self.handle_teacher_update_info()
            elif choice == 3:
                self.handle_teacher_view_salary()
            elif choice == 4:
                self.handle_teacher_view_courses()
            elif choice == 5:
                self.handle_change_password()
            elif choice == 6:
                self.handle_logout()
                break
    
    def show_admin_menu(self):
        """Display admin-specific menu."""
        while self.current_user and self.current_user.is_logged_in:
            self.clear_screen()
            self.current_user.display_menu()
            
            choice = self.get_user_input("Select an option", int,
                                       lambda x: 1 <= x <= 8)
            
            if choice is None:
                continue
            
            if choice == 1:
                self.handle_admin_create_user()
            elif choice == 2:
                self.handle_admin_delete_user()
            elif choice == 3:
                self.handle_admin_view_data()
            elif choice == 4:
                self.handle_admin_manage_enrollments()
            elif choice == 5:
                self.handle_admin_view_statistics()
            elif choice == 6:
                self.handle_admin_view_logs()
            elif choice == 7:
                self.handle_change_password()
            elif choice == 8:
                self.handle_logout()
                break
    
    # Student menu handlers
    def handle_student_enroll_course(self):
        """Handle student course enrollment."""
        self.clear_screen()
        self.print_header("Course Enrollment")
        
        # Display available courses
        courses = self.system_manager.get_available_courses()
        if not courses:
            print("No courses available.")
            input("Press Enter to continue...")
            return
        
        print("Available Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course.course_name} ({course.course_id}) - "
                  f"Instructor: {course.instructor} - "
                  f"Available: {course.get_available_spots()}/{course.capacity}")
        
        course_num = self.get_user_input("Select course number", int,
                                       lambda x: 1 <= x <= len(courses))
        
        if course_num is None:
            return
        
        selected_course = courses[course_num - 1]
        success = self.system_manager.enroll_student_in_course(
            self.current_user.student_id, selected_course.course_id)
        
        if success:
            print("Enrollment successful!")
        else:
            print("Enrollment failed.")
        
        input("Press Enter to continue...")
    
    def handle_student_unenroll_course(self):
        """Handle student course unenrollment."""
        self.clear_screen()
        self.print_header("Course Unenrollment")
        
        enrolled_courses = self.current_user.get_enrolled_courses()
        if not enrolled_courses:
            print("You are not enrolled in any courses.")
            input("Press Enter to continue...")
            return
        
        print("Your Enrolled Courses:")
        course_details = []
        for i, course_id in enumerate(enrolled_courses, 1):
            course = self.system_manager.get_course_by_id(course_id)
            if course:
                course_details.append(course)
                print(f"{i}. {course.course_name} ({course.course_id})")
        
        course_num = self.get_user_input("Select course number to unenroll", int,
                                       lambda x: 1 <= x <= len(course_details))
        
        if course_num is None:
            return
        
        selected_course = course_details[course_num - 1]
        success = self.system_manager.unenroll_student_from_course(
            self.current_user.student_id, selected_course.course_id)
        
        if success:
            print("Unenrollment successful!")
        else:
            print("Unenrollment failed.")
        
        input("Press Enter to continue...")
    
    def handle_student_view_records(self):
        """Handle viewing student academic records."""
        self.clear_screen()
        self.print_header("Academic Records")
        self.current_user.view_records()
        input("\nPress Enter to continue...")
    
    def handle_student_plot_cgpa(self):
        """Handle CGPA plotting."""
        self.clear_screen()
        self.print_header("CGPA Trend Graph")
        try:
            self.current_user.plot_cgpa()
            input("Press Enter after viewing the graph...")
        except Exception as e:
            print(f"Error displaying graph: {e}")
            input("Press Enter to continue...")
    
    def handle_student_view_teacher(self):
        """Handle viewing teacher profiles."""
        self.clear_screen()
        self.print_header("Teacher Profiles")
        
        teachers = self.system_manager.get_all_teachers()
        if not teachers:
            print("No teachers found.")
            input("Press Enter to continue...")
            return
        
        print("Available Teachers:")
        for i, teacher in enumerate(teachers, 1):
            print(f"{i}. {teacher.name} ({teacher.teacher_id}) - {teacher.department}")
        
        teacher_num = self.get_user_input("Select teacher number to view profile", int,
                                        lambda x: 1 <= x <= len(teachers))
        
        if teacher_num is None:
            return
        
        selected_teacher = teachers[teacher_num - 1]
        selected_teacher.view_profile()
        input("\nPress Enter to continue...")
    
    def handle_student_view_courses(self):
        """Handle viewing enrolled courses."""
        self.clear_screen()
        self.print_header("Your Enrolled Courses")
        
        enrolled_courses = self.current_user.get_enrolled_courses()
        if not enrolled_courses:
            print("You are not enrolled in any courses.")
        else:
            for course_id in enrolled_courses:
                course = self.system_manager.get_course_by_id(course_id)
                if course:
                    print(course.get_info())
        
        input("Press Enter to continue...")
    
    # Teacher menu handlers
    def handle_teacher_view_profile(self):
        """Handle viewing teacher profile."""
        self.clear_screen()
        self.print_header("Your Profile")
        self.current_user.view_profile()
        input("\nPress Enter to continue...")
    
    def handle_teacher_update_info(self):
        """Handle updating teacher information."""
        self.clear_screen()
        self.print_header("Update Personal Information")
        
        print("What would you like to update?")
        print("1. Name")
        print("2. Department")
        print("3. Qualification")
        print("4. Contact Information")
        print("5. Cancel")
        
        choice = self.get_user_input("Select option", int, lambda x: 1 <= x <= 5)
        
        if choice is None or choice == 5:
            return
        
        if choice == 1:
            new_name = self.get_user_input("Enter new name")
            if new_name:
                self.current_user.update_info('name', new_name)
        elif choice == 2:
            new_dept = self.get_user_input("Enter new department")
            if new_dept:
                self.current_user.update_info('department', new_dept)
        elif choice == 3:
            new_qual = self.get_user_input("Enter new qualification")
            if new_qual:
                self.current_user.update_info('qualification', new_qual)
        elif choice == 4:
            contact_type = self.get_user_input("Contact type (phone/address/etc.)")
            contact_value = self.get_user_input("Contact value")
            if contact_type and contact_value:
                self.current_user.update_info('contact_info', {contact_type: contact_value})
        
        input("Press Enter to continue...")
    
    def handle_teacher_view_salary(self):
        """Handle viewing salary information."""
        self.clear_screen()
        self.print_header("Salary Information")
        self.current_user.view_salary()
        input("\nPress Enter to continue...")
    
    def handle_teacher_view_courses(self):
        """Handle viewing taught courses."""
        self.clear_screen()
        self.print_header("Your Courses")
        
        if self.current_user.courses_taught:
            for course_id in self.current_user.courses_taught:
                course = self.system_manager.get_course_by_id(course_id)
                if course:
                    print(course.get_info())
        else:
            print("You are not assigned to any courses.")
        
        input("Press Enter to continue...")
    
    # Admin menu handlers
    def handle_admin_create_user(self):
        """Handle creating new users."""
        self.clear_screen()
        self.print_header("Create New User")
        
        print("Select user type:")
        print("1. Student")
        print("2. Teacher")
        print("3. Admin")
        
        user_type_choice = self.get_user_input("Select option", int, lambda x: 1 <= x <= 3)
        
        if user_type_choice is None:
            return
        
        user_types = {1: "Student", 2: "Teacher", 3: "Admin"}
        user_type = user_types[user_type_choice]
        
        name = self.get_user_input("Enter full name")
        email = self.get_user_input("Enter email")
        
        if not name or not email:
            print("Name and email are required.")
            input("Press Enter to continue...")
            return
        
        kwargs = {}
        if user_type == "Teacher":
            department = self.get_user_input("Enter department")
            salary = self.get_user_input("Enter salary", float)
            kwargs = {"department": department, "salary": salary}
        
        user_data = self.current_user.create_user(user_type, name, email, **kwargs)
        self.system_manager.save_user(user_data)
        
        input("Press Enter to continue...")
    
    def handle_admin_delete_user(self):
        """Handle deleting users."""
        self.clear_screen()
        self.print_header("Delete User")
        
        user_id = self.get_user_input("Enter User ID to delete")
        if user_id:
            confirm = self.get_user_input(f"Are you sure you want to delete user {user_id}? (yes/no)")
            if confirm.lower() == 'yes':
                success = self.current_user.delete_user(user_id, self.system_manager)
                if not success:
                    print("Failed to delete user.")
            else:
                print("Deletion cancelled.")
        
        input("Press Enter to continue...")
    
    def handle_admin_view_data(self):
        """Handle viewing all system data."""
        self.clear_screen()
        self.print_header("System Data Overview")
        self.current_user.view_all_data(self.system_manager)
        input("\nPress Enter to continue...")
    
    def handle_admin_manage_enrollments(self):
        """Handle managing enrollments."""
        self.clear_screen()
        self.print_header("Enrollment Management")
        self.current_user.manage_enrollments(self.system_manager)
        input("\nPress Enter to continue...")
    
    def handle_admin_view_statistics(self):
        """Handle viewing system statistics."""
        self.clear_screen()
        self.print_header("System Statistics")
        self.current_user.view_statistics(self.system_manager)
        input("\nPress Enter to continue...")
    
    def handle_admin_view_logs(self):
        """Handle viewing system logs."""
        self.clear_screen()
        self.print_header("System Logs")
        self.current_user.view_logs()
        input("\nPress Enter to continue...")
    
    # Common handlers
    def handle_change_password(self):
        """Handle password change."""
        self.clear_screen()
        self.print_header("Change Password")
        
        old_password = self.get_user_input("Enter current password")
        new_password = self.get_user_input("Enter new password")
        confirm_password = self.get_user_input("Confirm new password")
        
        if new_password != confirm_password:
            print("Passwords do not match.")
            input("Press Enter to continue...")
            return
        
        success = self.current_user.change_password(old_password, new_password)
        if success:
            self.system_manager.save_user_data()
        
        input("Press Enter to continue...")
    
    def handle_logout(self):
        """Handle user logout."""
        if self.current_user:
            self.current_user.logout()
            self.system_manager.save_user_data()
            self.current_user = None
        print("Logout successful.")
        input("Press Enter to continue...")
