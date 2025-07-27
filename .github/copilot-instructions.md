<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Portal System - Copilot Instructions

This is a Python Object-Oriented Programming (OOP) based console portal system for educational institutions.

## Project Structure

- **models/**: Contains all class definitions (User, Student, Teacher, Admin, Course, SalarySlip)
- **utils/**: Utility classes for file management, data validation, and menu handling
- **data/**: JSON files for data persistence
- **main.py**: Application entry point
- **system_manager.py**: Central system coordination

## Key OOP Concepts Implemented

- **Inheritance**: User base class extended by Student, Teacher, Admin
- **Encapsulation**: Private attributes with getter/setter methods
- **Polymorphism**: Method overriding (display_menu, get_user_type)
- **Abstraction**: Abstract User class with abstract methods

## Code Style Guidelines

- Use descriptive variable and method names
- Follow Python PEP 8 conventions
- Include comprehensive docstrings for all classes and methods
- Implement proper error handling with try-catch blocks
- Use type hints where appropriate

## System Features

- Role-based authentication and authorization
- Course enrollment/unenrollment with capacity management
- Academic record tracking and CGPA visualization
- Teacher profile and salary management
- Admin user creation and system monitoring
- File-based data persistence with backup functionality

## Dependencies

- matplotlib: For CGPA trend visualization
- Standard library: json, os, datetime, hashlib, string, re

## Security Considerations

- Passwords are hashed using SHA-256
- Input validation and sanitization implemented
- Role-based access control enforced
- Sensitive data encapsulated in private attributes

When suggesting code improvements or new features, ensure they:
1. Follow OOP principles
2. Maintain data integrity
3. Include proper error handling
4. Are consistent with existing code style
5. Include appropriate documentation
