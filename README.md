# 🎓 Portal System - Complete Documentation

*A comprehensive Python OOP-based educational portal system*

---

## 📋 Table of Contents

1. [System Overview](#-system-overview)
2. [System Architecture](#-system-architecture)
3. [File Structure](#-file-structure)
4. [Data Flow](#-data-flow)
5. [User Types & Functionality](#-user-types--functionality)
6. [Core Components](#-core-components)
7. [Data Storage](#-data-storage)
8. [Function Call Chain](#-function-call-chain)
9. [Installation & Setup](#-installation--setup)
10. [Usage Guide](#-usage-guide)
11. [Technical Details](#-technical-details)

---

## 🎯 System Overview

The Portal System is a console-based educational management application built with Python OOP principles. It supports three user roles (Student, Teacher, Admin) with role-specific functionality, data persistence, automatic backups, and comprehensive user management.

### Key Features
- **Multi-role user system** (Student, Teacher, Administrator)
- **Course management** with enrollment and capacity tracking
- **Academic records** and CGPA calculation
- **Salary management** for teachers
- **Automatic data backup** system
- **Data export** functionality
- **Secure authentication** with password hashing
- **Input validation** and error handling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                           MAIN.PY                              │
│                      (Application Entry)                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    SYSTEM_MANAGER.PY                           │
│                     (Central Controller)                       │
└──────────┬─────────────────────────────────────┬────────────────┘
           │                                     │
┌──────────▼─────────┐                ┌─────────▼──────────────────┐
│   FILE_MANAGER     │                │      MENU_MANAGER          │
│   (Data Handler)   │                │   (User Interface)         │
└────────────────────┘                └────────────────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────────┐
│                        MODELS                                 │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  USER   │ │ STUDENT │ │ TEACHER │ │  ADMIN  │ │ COURSE  │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
└────────────────────────────────────────────────────────────────┘
           │
┌──────────▼─────────────────────────────────────────────────────┐
│                     DATA STORAGE                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │ JSON FILES   │ │   BACKUPS    │ │   EXPORTS    │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
└────────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure

```
assignment---1/
├── 📄 main.py                      # Application entry point
├── 📄 system_manager.py            # Central system controller
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Project documentation
│
├── 📁 models/                      # Data model classes
│   ├── 📄 __init__.py
│   ├── 📄 user.py                  # Base user class (abstract)
│   ├── 📄 student.py               # Student class
│   ├── 📄 teacher.py               # Teacher class
│   ├── 📄 admin.py                 # Administrator class
│   ├── 📄 course.py                # Course class
│   └── 📄 salary_slip.py           # Salary slip class
│
├── 📁 utils/                       # Utility modules
│   ├── 📄 __init__.py
│   ├── 📄 file_manager.py          # File operations & data persistence
│   ├── 📄 data_validator.py        # Input validation utilities
│   └── 📄 menu_manager.py          # User interface menus
│
├── 📁 data/                        # Data storage
│   ├── 📄 users.json               # User data (2270+ lines)
│   ├── 📄 courses.json             # Course data (178+ lines)
│   ├── 📄 academic_records.json    # Student academic records
│   ├── 📄 salary_slips.json        # Teacher salary information
│   ├── 📄 system_logs.json         # System activity logs
│   ├── 📄 config.json              # System configuration
│   └── 📁 backups/                 # Automatic backup files (280+ files)
│
└── 📁 exports/                     # Data export files
    └── 📄 users_export_*.csv       # User data exports
```

### File Usage Status

| File/Directory     | Status | Purpose                              |
|--------------------|--------|--------------------------------------|
| ✅ **Core Files**  | Active | Main application logic               |
| ✅ **Models**      | Active | All user types and course management |
| ✅ **Utils**       | Active | File handling, validation, menus     |
| ✅ **Data Files**  | Active | Primary data storage                 |
| ✅ **Backups**     | Active | Automatic backup system              |
| ✅ **Exports**     | Active | CSV export functionality             |

**Result: 🎯 All files are actively used - No dead code found!**

---

## 🔄 Data Flow

### 1. System Startup Flow
```
1. main.py starts
   ↓
2. Run system diagnostics
   ↓
3. Create SystemManager
   ↓
4. SystemManager creates FileManager
   ↓
5. Load data from JSON files
   ↓
6. Create MenuManager
   ↓
7. Show main menu to user
```

### 2. User Interaction Flow
```
1. User selects action from menu
   ↓
2. MenuManager processes input
   ↓
3. MenuManager calls SystemManager method
   ↓
4. SystemManager interacts with model objects
   ↓
5. Model objects perform business logic
   ↓
6. Changes saved to JSON files
   ↓
7. Automatic backup created
```

### 3. Data Persistence Flow
```
Python Objects ←→ JSON Files ←→ Backup Files
     ↑               ↑              ↑
   (Memory)      (Permanent)    (Safety)
```

---

## 👥 User Types & Functionality

### 🎓 Student Features
- **Authentication**: Secure login with password hashing
- **Course Management**: 
  - Enroll in courses (with capacity checking)
  - Unenroll from courses (with confirmation)
  - View enrolled courses
- **Academic Records**:
  - View grades by semester
  - Calculate CGPA
  - Plot performance graphs (matplotlib)
- **Profile Management**:
  - Update personal information
  - Change password
- **Teacher Information**: View teacher profiles (privacy-protected)

### 👨‍🏫 Teacher Features
- **Profile Management**:
  - Continuous editing workflow
  - Update personal information
  - Manage contact details (11 contact types)
  - Update qualifications
- **Salary Management**:
  - View salary slips
  - Track salary history
- **Course Management**:
  - View assigned courses
  - Track enrolled students
- **History Tracking**: View all profile updates with timestamps

### 🔧 Admin Features
- **User Management**:
  - Create student, teacher, and admin accounts
  - Auto-generate user IDs and passwords
  - View all user information
  - Delete user accounts
- **Course Management**:
  - Create and manage courses
  - Set course capacity and sections
  - Manage enrollments
- **System Administration**:
  - View system logs and statistics
  - Export user data to CSV
  - System backup management
  - View all teacher updates

---

## 🔧 Core Components

### 1. SystemManager (The Brain)
**File**: `system_manager.py`

**Purpose**: Central coordinator for all system operations

**Key Responsibilities**:
- User authentication and session management
- Data loading and saving
- Coordination between components
- System backup operations

**Key Methods**:
```python
def load_all_data()          # Load data from JSON files
def save_all_data()          # Save data to JSON files  
def authenticate_user()      # User login verification
def create_user()           # Create new user accounts
def backup_system()         # Create system backup
```

### 2. FileManager (Data Handler)
**File**: `utils/file_manager.py`

**Purpose**: Manages all file operations and data persistence

**Key Features**:
- JSON file read/write operations
- Automatic backup creation
- Data export functionality
- Directory management

**Key Methods**:
```python
def save_data(file_type, data)    # Save data to JSON
def load_data(file_type)          # Load data from JSON
def backup_data()                 # Create backup
def export_data()                 # Export to CSV
```

### 3. MenuManager (User Interface)
**File**: `utils/menu_manager.py`

**Purpose**: Handles all user interactions and menu systems

**Menu Hierarchy**:
```
Main Menu
├── Login
│   ├── Student Menu
│   ├── Teacher Menu
│   └── Admin Menu
└── Exit
```

### 4. User Models (Data Objects)

#### Base User Class
**File**: `models/user.py`
- Abstract base class for all users
- Common functionality: authentication, password management
- Security: Password hashing with SHA-256

#### Student Class
**File**: `models/student.py`
```python
class Student(User):
    - enrolled_courses: []      # List of course IDs
    - academic_records: {}      # Semester-wise grades
    - cgpa_history: []         # CGPA tracking
```

#### Teacher Class
**File**: `models/teacher.py`
```python
class Teacher(User):
    - department: str          # Teaching department
    - qualification: str       # Educational background
    - contact_info: {}        # Contact details
    - salary_slips: []        # Salary information
    - courses_taught: []      # Assigned courses
```

#### Admin Class
**File**: `models/admin.py`
```python
class Admin(User):
    - access_level: str       # Permission level
    - system_logs: []        # Activity tracking
```

### 5. Course Management
**File**: `models/course.py`
```python
class Course:
    - course_id: str          # Unique identifier
    - course_name: str        # Course title
    - instructor: str         # Teacher assigned
    - capacity: int          # Maximum students
    - section: str           # Course section
    - enrolled_students: []   # Student list
```

---

## 💾 Data Storage

### JSON File Structure

#### users.json
```json
[
  {
    "username": "admin",
    "password": "hashed_password",
    "name": "System Administrator", 
    "email": "admin@portal.edu",
    "user_id": "ADM001",
    "user_type": "Admin",
    "admin_id": "ADM001",
    "access_level": "full",
    "system_logs": [...]
  }
]
```

#### courses.json
```json
[
  {
    "course_id": "CS101",
    "course_name": "Introduction to Programming",
    "instructor": "Professor Name",
    "capacity": 30,
    "section": "A",
    "enrolled_students": ["STU001", "STU002"],
    "created_date": "2025-07-27T18:18:54.019072"
  }
]
```

#### config.json
```json
{
  "version": "1.0",
  "created": "2025-07-27T18:18:54.015587",
  "last_backup": "2025-07-29T01:27:42.546869"
}
```

### Backup System
- **Automatic**: Created before every data save operation
- **Naming**: `{file_type}_{timestamp}.json`
- **Location**: `data/backups/`
- **Retention**: All backups are kept (280+ files currently)

### Export System
- **Format**: CSV files
- **Location**: `exports/`
- **Content**: User data with role-specific information

---

## 🔗 Function Call Chain

### Example: Student Enrolling in Course

```
1. User Input
   ↓
2. MenuManager.show_student_menu()
   ↓
3. MenuManager.handle_student_enrollment()
   ↓
4. SystemManager.enroll_student_in_course()
   ↓
5. Course.add_student() + Student.enroll_course()
   ↓
6. SystemManager.save_all_data()
   ↓
7. FileManager.save_data()
   ↓
8. FileManager._create_backup()
```

### Example: Admin Creating User

```
1. Admin Menu Selection
   ↓
2. MenuManager.show_admin_menu()
   ↓
3. MenuManager.handle_create_user()
   ↓
4. SystemManager.create_user()
   ↓
5. User/Student/Teacher.__init__()
   ↓
6. Admin.log_action()
   ↓
7. SystemManager.save_all_data()
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone/Download the project**
   ```bash
   git clone https://github.com/Noorulain-Shahid/assignment---1.git
   cd assignment---1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Dependencies
- `matplotlib>=3.5.0` - For CGPA graph plotting

---

## 📖 Usage Guide

### First-Time Setup
1. Run `python main.py`
2. System will create default data files
3. Default admin account: `username: admin`, `password: admin123`

### Login Process
1. Select user type (Student/Teacher/Admin)
2. Enter username and password
3. Access role-specific menu

### Student Operations
```
Student Menu:
1. Enroll in Course
2. Unenroll from Course  
3. View Enrolled Courses
4. View Academic Records
5. Plot CGPA Graph
6. Change Password
7. Logout
```

### Teacher Operations
```
Teacher Menu:
1. View Profile
2. Update Profile Information
3. View Salary Information
4. View Courses Taught
5. Change Password
6. Logout
```

### Admin Operations
```
Admin Menu:
1. Create User Account
2. View All Users
3. Manage Courses
4. View System Statistics
5. Export Data
6. System Backup
7. Logout
```

---

## 🔧 Technical Details

### Security Features
- **Password Hashing**: SHA-256 with salt
- **Session Management**: Login state tracking
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Try-catch blocks for robust operation

### Validation System
**File**: `utils/data_validator.py`

**Y/N Input Validation**:
- Accepts: `y, yes, yeah, yep, true, 1` (for YES)
- Accepts: `n, no, nope, false, 0` (for NO)
- Case-insensitive
- Clear error messages

### Performance Features
- **In-memory operations**: Fast data manipulation
- **Batch saving**: All changes saved together
- **Lazy loading**: Data loaded only when needed

### Error Handling
- **Graceful degradation**: System continues operation on non-critical errors
- **User-friendly messages**: Clear error explanations
- **Recovery options**: Multiple ways to handle failures

---

## 📊 System Statistics

### Current Data Volume
- **Users**: 2,270+ lines of user data
- **Courses**: 178+ lines of course data  
- **Backup Files**: 280+ automatic backups
- **Export Files**: 4 CSV exports

### File Status Summary
| Component | Files | Status | Usage |
|-----------|-------|--------|-------|
| Core System | 4 | ✅ Active | Entry point & management |
| Models | 7 | ✅ Active | All user types & courses |
| Utilities | 4 | ✅ Active | File ops, validation, menus |
| Data Files | 6 | ✅ Active | Primary data storage |
| Backups | 280+ | ✅ Active | Automatic safety copies |
| Exports | 4 | ✅ Active | CSV data exports |

### Code Quality
- **Object-Oriented Design**: Proper inheritance and encapsulation
- **Separation of Concerns**: Each module has specific responsibility
- **DRY Principle**: No code duplication found
- **Maintainable**: Clear structure and documentation

---

## 🏆 Key Achievements

1. **Zero Dead Code**: All files and functions are actively used
2. **Robust Architecture**: Clean separation of concerns
3. **Data Safety**: Comprehensive backup system
4. **User Experience**: Intuitive menu system with validation
5. **Scalability**: Easy to add new features and user types
6. **Security**: Proper authentication and data protection

---

**Last Updated**: August 4, 2025  
**Project Status**: ✅ Active Development  
**Code Quality**: ⭐⭐⭐⭐⭐ Excellent
