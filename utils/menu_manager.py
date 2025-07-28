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
    
    def get_yes_no_input(self, prompt: str) -> bool:
        """
        Get validated yes/no input from user.
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            bool: True for yes, False for no, None if cancelled
        """
        valid_yes = ['y', 'yes', 'yeah', 'yep', 'true', '1']
        valid_no = ['n', 'no', 'nope', 'false', '0']
        
        while True:
            try:
                user_input = input(f"\n{prompt}: ").strip().lower()
                
                if user_input in valid_yes:
                    return True
                elif user_input in valid_no:
                    return False
                else:
                    print("❌ Invalid input! Please enter:")
                    print("   • For YES: y, yes, yeah, yep, true, 1")
                    print("   • For NO: n, no, nope, false, 0")
                    continue
                    
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
            
            # Check if this is the user's first login
            if user.first_login:
                self.handle_first_time_login()
            
            # Show user menu after login or first-time setup
            self.show_user_menu()
        else:
            print(f"\nInvalid credentials or incorrect user type.")
            input("Press Enter to continue...")
    
    def handle_first_time_login(self):
        """Handle first-time login process for new users."""
        self.clear_screen()
        self.print_header("First-Time Login Setup")
        
        print("Welcome to the Portal System! This appears to be your first login.")
        print("For security, please set a password of your choice.")
        
        # Password setup is mandatory for first login
        print("\nPlease set your password:")
        
        # Username will remain the one set by the admin
        new_username = self.current_user.username
        
        # Get new password
        while True:
            new_password = self.get_user_input("Enter new password")
            if not new_password:
                print("Password cannot be empty.")
                continue
                
            confirm_password = self.get_user_input("Confirm new password")
            if new_password != confirm_password:
                print("Passwords don't match. Please try again.")
                continue
            break
        
        # Update only the password
        # Direct password change without old password verification for first login
        self.current_user._password = self.current_user._hash_password(new_password)
            
        # Mark first login as complete
        self.current_user.first_login = False
        
        # Save the changes
        self.system_manager.save_all_data()
        
        print("\nYour password has been updated successfully!")
    
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
                                       lambda x: 1 <= x <= 10)
            
            if choice is None:
                continue
            
            # Admin functions
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
                self.handle_admin_view_student_data()
            elif choice == 9:
                self.handle_admin_view_teacher_data()
            elif choice == 10:
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
            print(f"{i}. {course.course_name} ({course.course_id})")
            print(f"   Instructor: {course.instructor}")
            print(f"   Section: {course.section}")
            print(f"   Available: {course.get_available_spots()}/{course.capacity} spots")
            print()
        
        print(f"{len(courses) + 1}. Cancel and return to main menu")
        
        course_num = self.get_user_input("Select course number to enroll (or cancel)", int,
                                       lambda x: 1 <= x <= len(courses) + 1)
        
        if course_num is None or course_num == len(courses) + 1:
            print("Enrollment cancelled. Returning to main menu...")
            input("Press Enter to continue...")
            return
        
        selected_course = courses[course_num - 1]
        
        # Check if already enrolled in any section of this course
        enrolled_section = self.system_manager.find_student_enrolled_section(
            self.current_user.student_id, selected_course.course_id)
        if enrolled_section:
            print(f"❌ You are already enrolled in {selected_course.course_name} - Section {enrolled_section}")
            input("Press Enter to continue...")
            return
        
        # Show course details and confirmation
        self.clear_screen()
        self.print_header("Confirm Enrollment")
        print("Course Details:")
        print(f"Course Name: {selected_course.course_name}")
        print(f"Course ID: {selected_course.course_id}")
        print(f"Instructor: {selected_course.instructor}")
        print(f"Section: {selected_course.section}")
        print(f"Available Spots: {selected_course.get_available_spots()}/{selected_course.capacity}")
        print()
        
        confirm = self.get_yes_no_input("Do you want to enroll in this course? (y/n)")
        
        if confirm is None:
            print("Enrollment cancelled.")
            input("Press Enter to continue...")
            return
        elif confirm:
            print("\nProcessing enrollment...")
            success = self.system_manager.enroll_student_in_course(
                self.current_user.student_id, selected_course.course_id, selected_course.section)
            
            if success:
                print("✅ Enrollment successful!")
                print(f"You have been enrolled in {selected_course.course_name} - Section {selected_course.section}")
            else:
                print("❌ Enrollment failed. The course may be full or unavailable.")
        else:
            print("Enrollment cancelled.")
        
        input("Press Enter to continue...")
    
    def handle_student_unenroll_course(self):
        """Handle student course unenrollment."""
        self.clear_screen()
        self.print_header("Course Unenrollment")
        
        # Get enrolled courses from system manager for accurate data
        enrolled_courses = []
        for course_key, course in self.system_manager.courses.items():
            if self.current_user.student_id in course.enrolled_students:
                enrolled_courses.append(course)
        
        if not enrolled_courses:
            print("You are not enrolled in any courses.")
            input("Press Enter to continue...")
            return
        
        print("Your Enrolled Courses:")
        for i, course in enumerate(enrolled_courses, 1):
            print(f"{i}. {course.course_name} ({course.course_id})")
            print(f"   Instructor: {course.instructor}")
            print(f"   Section: {course.section}")
            print()
        
        print(f"{len(enrolled_courses) + 1}. Cancel and return to main menu")
        
        course_num = self.get_user_input("Select course number to unenroll (or cancel)", int,
                                       lambda x: 1 <= x <= len(enrolled_courses) + 1)
        
        if course_num is None or course_num == len(enrolled_courses) + 1:
            print("Unenrollment cancelled. Returning to main menu...")
            input("Press Enter to continue...")
            return
        
        selected_course = enrolled_courses[course_num - 1]
        
        # Show course details and confirmation
        self.clear_screen()
        self.print_header("Confirm Unenrollment")
        print("Course Details:")
        print(f"Course Name: {selected_course.course_name}")
        print(f"Course ID: {selected_course.course_id}")
        print(f"Instructor: {selected_course.instructor}")
        print(f"Section: {selected_course.section}")
        print()
        print("⚠️  WARNING: Unenrolling from this course will:")
        print("   • Remove you from the course roster")
        print("   • Make your spot available to other students")
        print("   • You may need to re-enroll if the course becomes full")
        print()
        
        # Final confirmation
        confirm = self.get_yes_no_input("Are you sure you want to unenroll from this course? (y/n)")
        
        if confirm is None:
            print("Unenrollment cancelled.")
            input("Press Enter to continue...")
            return
        elif confirm:
            print("\nProcessing unenrollment...")
            success = self.system_manager.unenroll_student_from_course(
                self.current_user.student_id, selected_course.course_id)
            
            if success:
                print("✅ Unenrollment successful!")
                print(f"You have been removed from {selected_course.course_name} - Section {selected_course.section}")
            else:
                print("❌ Unenrollment failed. Please try again or contact administration.")
        else:
            print("Unenrollment cancelled. You remain enrolled in the course.")
        
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
        
        print(f"{len(teachers) + 1}. Cancel and return to main menu")
        
        teacher_num = self.get_user_input("Select teacher number to view profile (or cancel)", int,
                                        lambda x: 1 <= x <= len(teachers) + 1)
        
        if teacher_num is None or teacher_num == len(teachers) + 1:
            print("Cancelled. Returning to main menu...")
            input("Press Enter to continue...")
            return
        
        selected_teacher = teachers[teacher_num - 1]
        self.clear_screen()
        self.print_header(f"Teacher Profile - {selected_teacher.name}")
        
        # Use public profile method for students
        selected_teacher.view_public_profile()
        
        print("\n" + "="*50)
        print("Privacy Notice:")
        print("• Salary and personal contact information are private")
        print("• Only public professional information is shown")
        print("• For course-related queries, use official channels")
        print("="*50)
        
        input("\nPress Enter to continue...")
    
    def handle_student_view_courses(self):
        """Handle viewing enrolled courses."""
        self.clear_screen()
        self.print_header("Your Enrolled Courses")
        
        # Get enrolled courses from system manager for accurate section data
        enrolled_courses = []
        for course_key, course in self.system_manager.courses.items():
            if self.current_user.student_id in course.enrolled_students:
                enrolled_courses.append(course)
        
        if not enrolled_courses:
            print("You are not enrolled in any courses.")
        else:
            print("Course Information:")
            print("-" * 50)
            for course in enrolled_courses:
                print(f"Course Name: {course.course_name}")
                print(f"Course ID: {course.course_id}")
                print(f"Section: {course.section}")
                print(f"Instructor: {course.instructor}")
                print(f"Enrolled Students: {len(course.enrolled_students)}/{course.capacity}")
                print("-" * 50)
        
        input("Press Enter to continue...")
    
    # Teacher menu handlers
    def handle_teacher_view_profile(self):
        """Handle viewing teacher profile."""
        self.clear_screen()
        self.print_header("Your Profile")
        self.current_user.view_profile()
        input("\nPress Enter to continue...")
    
    def handle_teacher_update_info(self):
        """Handle updating teacher information with continuous editing."""
        while True:
            self.clear_screen()
            self.print_header("Update Personal Information")
            
            # Show current information
            print("Current Information:")
            print(f"Name: {self.current_user.name}")
            print(f"Department: {self.current_user.department}")
            print(f"Qualification: {self.current_user.qualification}")
            print(f"Email: {self.current_user.email}")
            
            if self.current_user.contact_info:
                print("Contact Information:")
                for key, value in self.current_user.contact_info.items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
            
            print("\n" + "-" * 50)
            print("What would you like to update?")
            print("1. Name")
            print("2. Department")
            print("3. Qualification")
            print("4. Email")
            print("5. Manage Contact Information")
            print("6. Save and Exit")
            print("-" * 50)
            
            choice = self.get_user_input("Select option (1-6)", int, lambda x: 1 <= x <= 6)
            
            if choice is None:
                continue
            elif choice == 6:
                print("Saving changes and returning to main menu...")
                # Save all changes
                self.system_manager.save_all_data()
                input("Press Enter to continue...")
                break
            
            # Handle the specific update
            update_successful = False
            
            if choice == 1:
                new_name = self.get_user_input("Enter new name")
                if new_name:
                    old_name = self.current_user.name
                    if self.current_user.update_info('name', new_name):
                        print(f"✅ Name updated from '{old_name}' to '{new_name}'")
                        update_successful = True
                    else:
                        print("❌ Failed to update name")
            
            elif choice == 2:
                new_dept = self.get_user_input("Enter new department")
                if new_dept:
                    old_dept = self.current_user.department
                    if self.current_user.update_info('department', new_dept):
                        print(f"✅ Department updated from '{old_dept}' to '{new_dept}'")
                        update_successful = True
                    else:
                        print("❌ Failed to update department")
            
            elif choice == 3:
                new_qual = self.get_user_input("Enter new qualification")
                if new_qual:
                    old_qual = self.current_user.qualification
                    if self.current_user.update_info('qualification', new_qual):
                        print(f"✅ Qualification updated from '{old_qual}' to '{new_qual}'")
                        update_successful = True
                    else:
                        print("❌ Failed to update qualification")
            
            elif choice == 4:
                new_email = self.get_user_input("Enter new email")
                if new_email:
                    old_email = self.current_user.email
                    if self.current_user.update_info('email', new_email):
                        print(f"✅ Email updated from '{old_email}' to '{new_email}'")
                        update_successful = True
                    else:
                        print("❌ Failed to update email")
            
            elif choice == 5:
                # Contact Information Management with its own continuous loop
                while True:
                    self.clear_screen()
                    self.print_header("Contact Information Management")
                    
                    print("📞 CONTACT INFORMATION MANAGEMENT")
                    print("="*60)
                    print("Manage all your contact information in one place.")
                    print("Add, update, or remove multiple contacts without exiting.")
                    print()
                    
                    print("📋 AVAILABLE CONTACT TYPES:")
                    contact_types = [
                        ("office_phone", "(555) 123-4567"),
                        ("personal_phone", "(555) 987-6543"),
                        ("office_room", "Room 101, Science Building"),
                        ("office_building", "Science Building, Floor 2"),
                        ("office_hours", "Mon-Wed 9:00-11:00 AM, Fri 2:00-4:00 PM"),
                        ("address", "123 Main St, City, State 12345"),
                        ("emergency_contact", "Jane Doe - (555) 111-2222"),
                        ("department_phone", "(555) 200-3000 ext. 1234"),
                        ("email_secondary", "john.doe.backup@university.edu"),
                        ("office_website", "https://university.edu/faculty/johndoe"),
                        ("custom_contact", "Enter your own contact type")
                    ]
                    
                    for i, (contact_type, example) in enumerate(contact_types, 1):
                        if contact_type == "custom_contact":
                            print(f"{i}. Custom Contact Type → {example}")
                        else:
                            print(f"{i}. {contact_type.replace('_', ' ').title()} → {example}")
                    
                    print(f"{len(contact_types) + 1}. Remove Contact Information")
                    print(f"{len(contact_types) + 2}. Save and Return to Main Menu")
                    print()
                    
                    print("📝 CURRENT CONTACT INFORMATION:")
                    if self.current_user.contact_info:
                        for i, (key, value) in enumerate(self.current_user.contact_info.items(), 1):
                            print(f"   • {key.replace('_', ' ').title()}: {value}")
                    else:
                        print("   No contact information currently stored.")
                    print()
                    
                    # Get contact management choice
                    max_choice = len(contact_types) + 2
                    contact_choice = self.get_user_input(f"Select option (1-{max_choice})", int,
                                                       lambda x: 1 <= x <= max_choice)
                    
                    if contact_choice is None:
                        continue
                    elif contact_choice == max_choice:  # Save and Return
                        print("\n💾 Saving contact information...")
                        self.system_manager.save_all_data()
                        print("✅ Contact information saved successfully!")
                        input("Press Enter to return to main update menu...")
                        break
                    elif contact_choice == max_choice - 1:  # Remove Contact
                        self._handle_contact_removal()
                        continue
                    else:  # Add/Update contact
                        contact_operation_successful = self._handle_contact_addition_update(contact_types, contact_choice)
                        if contact_operation_successful:
                            update_successful = True
                        
                        # Ask if user wants to continue managing contacts
                        continue_contacts = self.get_yes_no_input("\nWould you like to manage another contact? (y/n)")
                        if not continue_contacts:
                            print("\n💾 Saving contact information...")
                            self.system_manager.save_all_data()
                            print("✅ Contact information saved successfully!")
                            input("Press Enter to return to main update menu...")
                            break
                        else:
                            print("\n🔄 Continuing with contact management...")
            
            # For choices 1-4, add the continuation logic
            if choice in [1, 2, 3, 4] and 'update_successful' in locals() and update_successful:
                print("\n🔄 Update completed successfully!")
                print("💡 You can continue updating other information or save and exit when done.")
                
                # Ask if user wants to continue or go back to menu
                continue_choice = self.get_yes_no_input("\nWould you like to update something else? (y/n)")
                if continue_choice is None or not continue_choice:
                    print("\n💾 Saving all changes...")
                    self.system_manager.save_all_data()
                    print("✅ All changes saved successfully!")
                    input("Press Enter to return to main menu...")
                    break
                else:
                    print("\n🔄 Continuing with updates...")
    
    def _handle_contact_addition_update(self, contact_types, choice):
        """Handle adding or updating a specific contact."""
        if choice == len(contact_types):  # Custom contact type
            print("\n➕ CUSTOM CONTACT TYPE:")
            contact_type = self.get_user_input("Enter custom contact type (use underscores for spaces)")
            if not contact_type:
                print("❌ Contact type is required.")
                return False
            example_format = "Enter your custom format"
        else:
            contact_type, example_format = contact_types[choice - 1]
        
        # Show current value if updating
        current_value = self.current_user.contact_info.get(contact_type, "")
        if current_value:
            print(f"\n🔄 UPDATING EXISTING CONTACT:")
            print(f"Contact Type: {contact_type.replace('_', ' ').title()}")
            print(f"Current Value: {current_value}")
            print(f"Suggested Format: {example_format}")
        else:
            print(f"\n➕ ADDING NEW CONTACT:")
            print(f"Contact Type: {contact_type.replace('_', ' ').title()}")
            print(f"Suggested Format: {example_format}")
        
        contact_value = self.get_user_input(f"Enter value for {contact_type.replace('_', ' ').title()}")
        
        if contact_value:
            # Update contact information
            is_update = contact_type in self.current_user.contact_info
            old_value = self.current_user.contact_info.get(contact_type, "")
            
            if self.current_user.update_info('contact_info', {contact_type: contact_value}):
                if is_update:
                    print(f"\n✅ CONTACT UPDATED SUCCESSFULLY!")
                    print(f"   Type: {contact_type.replace('_', ' ').title()}")
                    print(f"   Old Value: {old_value}")
                    print(f"   New Value: {contact_value}")
                else:
                    print(f"\n✅ CONTACT ADDED SUCCESSFULLY!")
                    print(f"   Type: {contact_type.replace('_', ' ').title()}")
                    print(f"   Value: {contact_value}")
                return True
            else:
                print("❌ Failed to update contact information")
                return False
        else:
            print("❌ Contact value is required.")
            return False
    
    def _handle_contact_removal(self):
        """Handle removal of contact information."""
        if not self.current_user.contact_info:
            print("\n❌ No contact information to remove.")
            input("Press Enter to continue...")
            return
        
        print("\n📝 CURRENT CONTACT INFORMATION:")
        contact_items = list(self.current_user.contact_info.items())
        for i, (key, value) in enumerate(contact_items, 1):
            print(f"{i}. {key.replace('_', ' ').title()}: {value}")
        print(f"{len(contact_items) + 1}. Cancel (Go back without changes)")
        
        remove_choice = self.get_user_input("Select contact to remove or cancel", int,
                                          lambda x: 1 <= x <= len(contact_items) + 1)
        
        if remove_choice and remove_choice <= len(contact_items):
            # Confirm removal
            key_to_remove = contact_items[remove_choice - 1][0]
            contact_value = contact_items[remove_choice - 1][1]
            
            print(f"\nYou are about to remove:")
            print(f"Contact: {key_to_remove.replace('_', ' ').title()}")
            print(f"Value: {contact_value}")
            
            confirm = self.get_yes_no_input("Are you sure you want to remove this contact? (y/n)")
            if confirm is None:
                print("❌ Contact removal cancelled.")
            elif confirm:
                del self.current_user.contact_info[key_to_remove]
                print(f"✅ Removed contact information: {key_to_remove.replace('_', ' ').title()}")
            else:
                print("❌ Contact removal cancelled.")
        elif remove_choice == len(contact_items) + 1:
            print("❌ Contact removal cancelled. No changes made.")
        
        input("\nPress Enter to continue...")
    
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
        
        teacher_courses = []
        # Find all course sections taught by this teacher
        for course_key, course in self.system_manager.courses.items():
            if course.instructor == self.current_user.name:
                teacher_courses.append(course)
        
        if teacher_courses:
            for course in teacher_courses:
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
        
        # Ask admin to set username and password for the user
        print("\nPlease set the username and password for the user:")
        
        from utils.data_validator import DataValidator
        
        # Ask for username with option to generate automatically
        print("(Leave blank to generate a username automatically)")
        custom_username = self.get_user_input("Enter username")
        
        # If username is not blank, validate it
        if custom_username:
            validation_result = DataValidator.validate_username(custom_username)
            while not validation_result['valid']:
                print(f"Invalid username: {validation_result['message']}")
                custom_username = self.get_user_input("Enter username (or leave blank to generate automatically)")
                
                # If user decides to let system generate username
                if not custom_username:
                    break
                    
                validation_result = DataValidator.validate_username(custom_username)
            
        # Ask for password
        print("(Leave blank to generate a password automatically)")
        custom_password = self.get_user_input("Enter password")
        
        kwargs = {}
        if user_type == "Teacher":
            department = self.get_user_input("Enter department")
            
            # Get salary with validation to ensure it's not negative
            while True:
                salary = self.get_user_input("Enter salary", float)
                if salary is None:  # User cancelled
                    return
                    
                if salary < 0:
                    print("❌ Error: Salary cannot be negative. Please enter a valid amount.")
                    continue
                break
                
            kwargs = {"department": department, "salary": salary}
        
        user_data = self.current_user.create_user(
            user_type, name, email, 
            custom_username=custom_username, 
            custom_password=custom_password, 
            **kwargs
        )
        
        # Store the plain password before saving (as save_user might remove it)
        plain_password = user_data.get('plain_password', user_data['password'])
        
        if self.system_manager.save_user(user_data):
            print("\nUser created and saved successfully!")
            print(f"User information has been added to the system.")
            print(f"The user can now log in with:")
            print(f"  Username: {user_data['username']}")
            print(f"  Password: {plain_password}")
        else:
            print("\nFailed to save user. Username might already exist.")
            
        input("\nPress Enter to continue...")
    
    def handle_admin_delete_user(self):
        """Handle deleting users."""
        while True:
            self.clear_screen()
            self.print_header("Delete User")
            
            username = self.get_user_input("Enter username to delete (leave blank to cancel)")
            if not username:
                print("Operation cancelled.")
                break
                
            confirm = self.get_yes_no_input(f"Are you sure you want to delete user '{username}'? (y/n)")
            if confirm is None or not confirm:
                print("Deletion cancelled.")
            else:
                success = self.current_user.delete_user(username, self.system_manager)
                if success:
                    print(f"User '{username}' deleted successfully.")
                else:
                    print(f"Failed to delete user. Username '{username}' not found.")
            
            # Ask if admin wants to delete more users
            delete_more = self.get_yes_no_input("\nDo you want to delete more users? (y/n)")
            if not delete_more:
                break
        
        input("Press Enter to return to the admin menu...")
    
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
        
    def handle_admin_view_student_data(self):
        """Handle viewing student data."""
        self.clear_screen()
        self.print_header("Student Data")
        
        # Ask for student username
        username = self.get_user_input("\nEnter student username (or leave blank to cancel)")
        if not username:
            return
            
        # Find student by username
        student = None
        for user in self.system_manager.users.values():
            if user.__class__.__name__ == "Student" and user.username == username:
                student = user
                break
        
        if not student:
            print(f"No student found with username '{username}'.")
            input("\nPress Enter to continue...")
            return
        
        while True:
            self.clear_screen()
            self.print_header(f"Student: {student.name}")
            print(f"Username: {student.username}")
            print(f"Email: {student.email}")
            print(f"Student ID: {student.student_id}")
            
            # Display student options
            print("\nOptions:")
            print("1. View Academic Records")
            print("2. Plot CGPA Graph")
            print("3. View Enrolled Courses")
            print("4. Enroll Student in Course")
            print("5. Unenroll Student from Course")
            print("6. Change Student Password")
            print("7. Return to Admin Menu")
            
            sub_choice = self.get_user_input("\nSelect an option", int,
                                          lambda x: 1 <= x <= 7)
            
            if sub_choice is None:
                continue
            
            # Save current user temporarily
            original_user = self.current_user
            
            try:
                # Temporarily set the selected student as current user
                self.current_user = student
                
                if sub_choice == 1:
                    self.handle_student_view_records()
                elif sub_choice == 2:
                    self.handle_student_plot_cgpa()
                elif sub_choice == 3:
                    self.handle_student_view_courses()
                elif sub_choice == 4:
                    self.handle_student_enroll_course()
                elif sub_choice == 5:
                    self.handle_student_unenroll_course()
                elif sub_choice == 6:
                    # Special admin password change function
                    self.clear_screen()
                    self.print_header(f"Change Password for {student.username}")
                    new_password = self.get_user_input("Enter new password")
                    confirm_password = self.get_user_input("Confirm new password")
                    
                    if new_password != confirm_password:
                        print("Passwords do not match.")
                    elif not new_password:
                        print("Password cannot be empty.")
                    else:
                        # Admin can bypass old password check - directly set the hashed password
                        student._password = student._hash_password(new_password)
                        student.first_login = False
                        print(f"Password changed successfully for {student.username}.")
                        self.system_manager.save_user_data()
                        
                    input("Press Enter to continue...")
                elif sub_choice == 7:
                    break
            finally:
                # Restore original admin user
                self.current_user = original_user
        
        # Go back to admin menu
        return
        
    def handle_admin_view_teacher_data(self):
        """Handle viewing teacher data."""
        self.clear_screen()
        self.print_header("Teacher Data")
        
        # Ask for teacher username
        username = self.get_user_input("\nEnter teacher username (or leave blank to cancel)")
        if not username:
            return
            
        # Find teacher by username
        teacher = None
        for user in self.system_manager.users.values():
            if user.__class__.__name__ == "Teacher" and user.username == username:
                teacher = user
                break
        
        if not teacher:
            print(f"No teacher found with username '{username}'.")
            input("\nPress Enter to continue...")
            return
        
        while True:
            self.clear_screen()
            self.print_header(f"Teacher: {teacher.name}")
            print(f"Username: {teacher.username}")
            print(f"Email: {teacher.email}")
            print(f"Teacher ID: {teacher.teacher_id}")
            print(f"Department: {teacher.department}")
            print(f"Salary: ${teacher.salary:.2f}")
            
            # Display teacher options
            print("\nOptions:")
            print("1. View Profile")
            print("2. Update Teacher Information")
            print("3. View Salary Slips")
            print("4. View Courses Taught")
            print("5. Assign Course to Teacher")
            print("6. Change Teacher Password")
            print("7. Adjust Salary")
            print("8. Return to Admin Menu")
            
            sub_choice = self.get_user_input("\nSelect an option", int,
                                          lambda x: 1 <= x <= 8)
            
            if sub_choice is None:
                continue
            
            # Save current user temporarily
            original_user = self.current_user
            
            try:
                # Temporarily set the selected teacher as current user
                self.current_user = teacher
                
                if sub_choice == 1:
                    self.handle_teacher_view_profile()
                elif sub_choice == 2:
                    self.handle_teacher_update_info()
                    print(f"\nAdmin action: Updated information for teacher {teacher.username}")
                    input("Press Enter to continue...")
                elif sub_choice == 3:
                    self.handle_teacher_view_salary()
                elif sub_choice == 4:
                    self.handle_teacher_view_courses()
                elif sub_choice == 5:
                    # Admin assigns a course to teacher
                    self.clear_screen()
                    self.print_header(f"Assign Course to {teacher.name}")
                    
                    # Get all courses
                    courses = self.system_manager.get_all_courses()
                    if not courses:
                        print("No courses available in the system.")
                    else:
                        print("\nAvailable Courses:")
                        for i, course in enumerate(courses, 1):
                            print(f"{i}. {course.course_name} ({course.course_id}) - Section: {course.section}")
                        
                        course_num = self.get_user_input("\nSelect course number to assign (or 0 to cancel)", int,
                                                      lambda x: 0 <= x <= len(courses))
                        
                        if course_num and course_num > 0:
                            selected_course = courses[course_num - 1]
                            # Update course instructor
                            selected_course.instructor = teacher.name
                            selected_course.teacher_id = teacher.teacher_id
                            print(f"Course '{selected_course.course_name}' assigned to {teacher.name}.")
                            self.system_manager.save_course_data()
                            
                    input("Press Enter to continue...")
                elif sub_choice == 6:
                    # Special admin password change function
                    self.clear_screen()
                    self.print_header(f"Change Password for {teacher.username}")
                    new_password = self.get_user_input("Enter new password")
                    confirm_password = self.get_user_input("Confirm new password")
                    
                    if new_password != confirm_password:
                        print("Passwords do not match.")
                    elif not new_password:
                        print("Password cannot be empty.")
                    else:
                        # Admin can bypass old password check - directly set the hashed password
                        teacher._password = teacher._hash_password(new_password)
                        teacher.first_login = False
                        print(f"Password changed successfully for {teacher.username}.")
                        self.system_manager.save_user_data()
                        
                    input("Press Enter to continue...")
                elif sub_choice == 7:
                    # Adjust teacher salary
                    self.clear_screen()
                    self.print_header(f"Adjust Salary for {teacher.name}")
                    print(f"Current Salary: ${teacher.salary:.2f}")
                    
                    new_salary = self.get_user_input("Enter new salary amount", float, 
                                                  lambda x: x >= 0)  # Ensuring non-negative salary
                    
                    if new_salary is not None:
                        teacher.salary = new_salary
                        print(f"Salary updated to ${teacher.salary:.2f}")
                        self.system_manager.save_user_data()
                    else:
                        print("Invalid salary amount. Salary not updated.")
                    
                    input("Press Enter to continue...")
                elif sub_choice == 8:
                    break
            finally:
                # Restore original admin user
                self.current_user = original_user
        
        # Go back to admin menu
        return
        
    def handle_admin_export_users(self):
        """Handle exporting all user data."""
        self.clear_screen()
        self.print_header("Export Users Data")
        
        # Get all users from the system
        all_users = self.system_manager.get_all_users_data()
        
        if not all_users:
            print("No users found in the system.")
            input("\nPress Enter to continue...")
            return
            
        print(f"Found {len(all_users)} users in the system.")
        
        # Ask for custom filename or use default
        print("\nExport options:")
        print("1. Use default filename (recommended)")
        print("2. Specify custom filename")
        
        option = self.get_user_input("Select option", int, lambda x: x in [1, 2])
        
        file_path = None
        if option == 2:
            filename = self.get_user_input("Enter filename (without extension)")
            if filename:
                import os
                export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exports')
                file_path = os.path.join(export_dir, f"{filename}.csv")
        
        # Export the data
        success, result = self.current_user.export_users_data(all_users, file_path)
        
        if success:
            print(f"\n✓ User data exported successfully!")
            print(f"File saved to: {result}")
        else:
            print(f"\n❌ Failed to export user data:")
            print(f"Error: {result}")
            
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
