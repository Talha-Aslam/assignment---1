# Console-Based Portal System

A comprehensive Python OOP-based portal system supporting three user roles: Student, Teacher, and Administrator.

## Features

### Student Features
- Enroll in course sections (with capacity restrictions)
- View academic records and CGPA per semester
- Plot academic performance graphs using matplotlib
- Unenroll from courses
- Change passwords
- View teacher profiles

### Teacher Features
- View salary slips
- Add, update, and delete personal information
- Change passwords
- Manage profile and qualification details

### Admin Features
- Full access to all student and teacher data
- Create auto-generated IDs and passwords for users
- View all updates made by teachers
- Manage enrollments and user accounts
- View system statistics and logs

## Technical Implementation

### OOP Concepts Used
- **Inheritance**: User base class with Student, Teacher, Admin subclasses
- **Encapsulation**: Secure sensitive data with private attributes
- **Polymorphism**: Method overriding for role-specific behaviors
- **Abstraction**: Abstract User class and interface definitions

### Data Management
- File handling for persistent storage
- JSON format for structured data
- Backup and recovery mechanisms
- Data validation and sanitization

### Dependencies
- `matplotlib` for plotting CGPA trends
- `json` for data serialization
- `datetime` for timestamps
- `hashlib` for password security

## Project Structure
```
portal_system/
├── main.py              # Main application entry point
├── models/
│   ├── user.py          # Base User class
│   ├── student.py       # Student class
│   ├── teacher.py       # Teacher class
│   ├── admin.py         # Admin class
│   ├── course.py        # Course management
│   └── salary_slip.py   # Salary slip handling
├── utils/
│   ├── file_manager.py  # File operations
│   ├── data_validator.py # Input validation
│   └── menu_manager.py  # Menu systems
├── data/
│   ├── users.json       # User credentials
│   ├── courses.json     # Course data
│   ├── records.json     # Academic records
│   └── salary_slips.json # Salary information
└── UML_Class_Diagram.py # System design
```

## Installation and Setup

1. Clone or download the project
2. Install required dependencies:
   ```bash
   pip install matplotlib
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Quick Demo

To see a quick demonstration of system features:
```bash
python demo.py
```

To view the UML Class Diagram:
```bash
python UML_Class_Diagram.py
```

## Usage

1. Start the application
2. Login with your credentials (or use default accounts)
3. Navigate through role-specific menus
4. Perform desired operations

## Default Accounts

### Students (10 accounts)
- Username: student1-student10
- Password: pass123 (for all)

### Teachers (10 accounts)
- Username: teacher1-teacher10
- Password: teach123 (for all)

### Admin
- Username: admin
- Password: admin123

## System Requirements

- Python 3.7+
- matplotlib library
- Console/Terminal access
- Windows/Linux/MacOS compatible
