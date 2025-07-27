"""
UML Class Diagram for Console-Based Portal System

This file contains a visual representation of the UML Class Diagram using ASCII art
and detailed class specifications for the portal system.

=================================================================================================
                                    UML CLASS DIAGRAM
=================================================================================================

                                      ┌─────────────────┐
                                      │      User       │
                                      │   (Abstract)    │
                                      ├─────────────────┤
                                      │ - username: str │
                                      │ - password: str │
                                      │ - name: str     │
                                      │ - email: str    │
                                      │ - user_id: str  │
                                      ├─────────────────┤
                                      │ + login()       │
                                      │ + logout()      │
                                      │ + change_password() │
                                      │ + display_menu()│
                                      │ + validate_credentials() │
                                      └─────────────────┘
                                              △
                                              │
                          ┌───────────────────┼───────────────────┐
                          │                   │                   │
                ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
                │    Student      │ │    Teacher      │ │    Admin        │
                ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
                │ - student_id    │ │ - teacher_id    │ │ - admin_id      │
                │ - enrolled_courses │ │ - department  │ │ - access_level  │
                │ - academic_records │ │ - salary      │ │ - system_logs   │
                │ - cgpa_history  │ │ - qualification │ │                 │
                │ - semester_data │ │ - contact_info  │ │                 │
                ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
                │ + enroll_course()│ │ + view_salary() │ │ + create_user() │
                │ + unenroll_course()│ │ + update_info()│ │ + delete_user() │
                │ + view_records()│ │ + view_profile()│ │ + view_all_data()│
                │ + plot_cgpa()   │ │ + display_menu()│ │ + manage_enrollments()│
                │ + view_teacher_profile()│ │ + change_password()│ │ + view_statistics()│
                │ + display_menu()│ │                 │ │ + view_logs()   │
                └─────────────────┘ └─────────────────┘ │ + display_menu()│
                         │                   │         └─────────────────┘
                         │                   │                   │
                         ▼                   ▼                   ▼
                ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
                │    Course       │ │   SalarySlip    │ │   SystemLog     │
                ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
                │ - course_id     │ │ - slip_id       │ │ - log_id        │
                │ - course_name   │ │ - teacher_id    │ │ - timestamp     │
                │ - instructor    │ │ - month         │ │ - action        │
                │ - capacity      │ │ - basic_salary  │ │ - user_id       │
                │ - enrolled_students│ │ - allowances  │ │ - details       │
                │ - section       │ │ - deductions    │ │                 │
                ├─────────────────┤ │ - net_salary    │ ├─────────────────┤
                │ + add_student() │ ├─────────────────┤ │ + log_action()  │
                │ + remove_student()│ │ + calculate_net()│ │ + get_logs()   │
                │ + is_full()     │ │ + display()     │ │ + filter_logs() │
                │ + get_info()    │ │ + save_to_file()│ └─────────────────┘
                └─────────────────┘ └─────────────────┘

                ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
                │  FileManager    │ │   DataValidator │ │   MenuManager   │
                ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
                │ - file_paths    │ │                 │ │ - current_user  │
                ├─────────────────┤ ├─────────────────┤ ├─────────────────┤
                │ + save_data()   │ │ + validate_email()│ │ + show_student_menu()│
                │ + load_data()   │ │ + validate_id() │ │ + show_teacher_menu()│
                │ + backup_data() │ │ + validate_cgpa()│ │ + show_admin_menu()│
                │ + initialize_files()│ │ + sanitize_input()│ │ + handle_choice()│
                └─────────────────┘ └─────────────────┘ └─────────────────┘

=================================================================================================
                                  CLASS RELATIONSHIPS
=================================================================================================

1. INHERITANCE:
   - User (Abstract Base Class)
     ├── Student (inherits from User)
     ├── Teacher (inherits from User)
     └── Admin (inherits from User)

2. COMPOSITION:
   - Student HAS-A list of Course objects (enrolled_courses)
   - Teacher HAS-A list of SalarySlip objects
   - Admin HAS-A list of SystemLog objects

3. AGGREGATION:
   - Course contains references to Student objects (enrolled_students)
   - SystemLog references User objects (user_id)

4. DEPENDENCY:
   - All classes depend on FileManager for data persistence
   - All classes use DataValidator for input validation
   - All user classes interact with MenuManager

=================================================================================================
                                  KEY OOP CONCEPTS
=================================================================================================

1. INHERITANCE:
   - User class serves as base class with common attributes and methods
   - Student, Teacher, Admin inherit and extend User functionality
   - Method overriding in display_menu() for role-specific behavior

2. ENCAPSULATION:
   - Private attributes (prefixed with _) for sensitive data
   - Public methods provide controlled access to data
   - Password and ID validation through methods

3. POLYMORPHISM:
   - display_menu() method behaves differently for each user type
   - login() method can be overridden for role-specific login logic
   - File handling methods adapt to different data types

4. ABSTRACTION:
   - User class is abstract (cannot be instantiated directly)
   - Common interface for all user types through base class
   - FileManager abstracts file operations from business logic

=================================================================================================
"""

# Additional UML notation explanations
UML_SYMBOLS = {
    "△": "Inheritance (IS-A relationship)",
    "◇": "Aggregation (HAS-A relationship, weak)",
    "◆": "Composition (HAS-A relationship, strong)",
    "→": "Dependency (USES-A relationship)",
    "+": "Public method/attribute",
    "-": "Private method/attribute",
    "#": "Protected method/attribute",
    "<<abstract>>": "Abstract class",
    "<<interface>>": "Interface"
}

def display_uml_legend():
    """Display UML notation legend"""
    print("\n" + "="*50)
    print("UML NOTATION LEGEND")
    print("="*50)
    for symbol, meaning in UML_SYMBOLS.items():
        print(f"{symbol:10} : {meaning}")
    print("="*50)

if __name__ == "__main__":
    print(__doc__)
    display_uml_legend()
