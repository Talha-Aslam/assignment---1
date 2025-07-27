"""
Data Validator utility for input validation and sanitization
"""

import re
import string
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class DataValidator:
    """
    Provides data validation and sanitization methods for the portal system.
    Ensures data integrity and security across all user inputs.
    """
    
    # Regular expressions for validation
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$'
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'
    PASSWORD_MIN_LENGTH = 6
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        
        return bool(re.match(DataValidator.EMAIL_PATTERN, email.strip()))
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Union[bool, str]]:
        """
        Validate username format and requirements.
        
        Args:
            username (str): Username to validate
            
        Returns:
            dict: Validation result with status and message
        """
        if not username or not isinstance(username, str):
            return {'valid': False, 'message': 'Username cannot be empty'}
        
        username = username.strip()
        
        if len(username) < 3:
            return {'valid': False, 'message': 'Username must be at least 3 characters long'}
        
        if len(username) > 20:
            return {'valid': False, 'message': 'Username cannot exceed 20 characters'}
        
        if not re.match(DataValidator.USERNAME_PATTERN, username):
            return {'valid': False, 'message': 'Username can only contain letters, numbers, and underscores'}
        
        if username[0].isdigit():
            return {'valid': False, 'message': 'Username cannot start with a number'}
        
        return {'valid': True, 'message': 'Valid username'}
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, Union[bool, str, int]]:
        """
        Validate password strength and requirements.
        
        Args:
            password (str): Password to validate
            
        Returns:
            dict: Validation result with status, message, and strength score
        """
        if not password or not isinstance(password, str):
            return {'valid': False, 'message': 'Password cannot be empty', 'strength': 0}
        
        strength_score = 0
        issues = []
        
        # Length check
        if len(password) < DataValidator.PASSWORD_MIN_LENGTH:
            issues.append(f'Password must be at least {DataValidator.PASSWORD_MIN_LENGTH} characters long')
        else:
            strength_score += 1
        
        # Character type checks
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if has_lower:
            strength_score += 1
        else:
            issues.append('Password should contain lowercase letters')
        
        if has_upper:
            strength_score += 1
        else:
            issues.append('Password should contain uppercase letters')
        
        if has_digit:
            strength_score += 1
        else:
            issues.append('Password should contain numbers')
        
        if has_special:
            strength_score += 1
        else:
            issues.append('Password should contain special characters')
        
        # Length bonus
        if len(password) >= 12:
            strength_score += 1
        
        # No common patterns
        common_patterns = ['123', 'abc', 'password', 'admin', 'user']
        if any(pattern in password.lower() for pattern in common_patterns):
            strength_score -= 1
            issues.append('Password contains common patterns')
        
        is_valid = len(issues) == 0 and strength_score >= 3
        
        return {
            'valid': is_valid,
            'message': '; '.join(issues) if issues else 'Password meets requirements',
            'strength': max(0, strength_score),
            'issues': issues
        }
    
    @staticmethod
    def validate_name(name: str) -> Dict[str, Union[bool, str]]:
        """
        Validate person name.
        
        Args:
            name (str): Name to validate
            
        Returns:
            dict: Validation result
        """
        if not name or not isinstance(name, str):
            return {'valid': False, 'message': 'Name cannot be empty'}
        
        name = name.strip()
        
        if len(name) < 2:
            return {'valid': False, 'message': 'Name must be at least 2 characters long'}
        
        if len(name) > 50:
            return {'valid': False, 'message': 'Name cannot exceed 50 characters'}
        
        # Allow letters, spaces, hyphens, apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            return {'valid': False, 'message': 'Name can only contain letters, spaces, hyphens, and apostrophes'}
        
        # Check for reasonable number of words
        words = name.split()
        if len(words) > 5:
            return {'valid': False, 'message': 'Name cannot have more than 5 words'}
        
        return {'valid': True, 'message': 'Valid name'}
    
    @staticmethod
    def validate_phone(phone: str) -> Dict[str, Union[bool, str]]:
        """
        Validate phone number.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            dict: Validation result
        """
        if not phone or not isinstance(phone, str):
            return {'valid': False, 'message': 'Phone number cannot be empty'}
        
        # Remove all non-digit characters for length check
        digits_only = re.sub(r'\D', '', phone)
        
        if len(digits_only) < 10:
            return {'valid': False, 'message': 'Phone number must have at least 10 digits'}
        
        if len(digits_only) > 15:
            return {'valid': False, 'message': 'Phone number cannot have more than 15 digits'}
        
        if re.match(DataValidator.PHONE_PATTERN, phone):
            return {'valid': True, 'message': 'Valid phone number'}
        else:
            return {'valid': False, 'message': 'Invalid phone number format'}
    
    @staticmethod
    def validate_cgpa(cgpa: Union[str, float, int]) -> Dict[str, Union[bool, str, float]]:
        """
        Validate CGPA value.
        
        Args:
            cgpa: CGPA value to validate
            
        Returns:
            dict: Validation result with normalized value
        """
        try:
            cgpa_float = float(cgpa)
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'CGPA must be a number', 'value': 0.0}
        
        if cgpa_float < 0:
            return {'valid': False, 'message': 'CGPA cannot be negative', 'value': 0.0}
        
        if cgpa_float > 4.0:
            return {'valid': False, 'message': 'CGPA cannot exceed 4.0', 'value': 4.0}
        
        # Round to 2 decimal places
        cgpa_rounded = round(cgpa_float, 2)
        
        return {'valid': True, 'message': 'Valid CGPA', 'value': cgpa_rounded}
    
    @staticmethod
    def validate_grade(grade: str) -> Dict[str, Union[bool, str]]:
        """
        Validate academic grade.
        
        Args:
            grade (str): Grade to validate
            
        Returns:
            dict: Validation result
        """
        if not grade or not isinstance(grade, str):
            return {'valid': False, 'message': 'Grade cannot be empty'}
        
        grade = grade.strip().upper()
        valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F', 'W', 'I']
        
        if grade in valid_grades:
            return {'valid': True, 'message': 'Valid grade', 'normalized': grade}
        else:
            return {'valid': False, 'message': f'Invalid grade. Valid grades: {", ".join(valid_grades)}'}
    
    @staticmethod
    def validate_salary(salary: Union[str, float, int]) -> Dict[str, Union[bool, str, float]]:
        """
        Validate salary amount.
        
        Args:
            salary: Salary value to validate
            
        Returns:
            dict: Validation result with normalized value
        """
        try:
            salary_float = float(salary)
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Salary must be a number', 'value': 0.0}
        
        if salary_float < 0:
            return {'valid': False, 'message': 'Salary cannot be negative', 'value': 0.0}
        
        if salary_float > 1000000:  # Reasonable upper limit
            return {'valid': False, 'message': 'Salary seems unreasonably high', 'value': salary_float}
        
        # Round to 2 decimal places
        salary_rounded = round(salary_float, 2)
        
        return {'valid': True, 'message': 'Valid salary', 'value': salary_rounded}
    
    @staticmethod
    def sanitize_input(input_string: str, max_length: int = 255) -> str:
        """
        Sanitize input string by removing dangerous characters and limiting length.
        
        Args:
            input_string (str): String to sanitize
            max_length (int): Maximum allowed length
            
        Returns:
            str: Sanitized string
        """
        if not input_string or not isinstance(input_string, str):
            return ""
        
        # Remove null bytes and control characters (except common whitespace)
        sanitized = ''.join(char for char in input_string 
                          if ord(char) >= 32 or char in '\t\n\r')
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def validate_date(date_string: str, date_format: str = "%Y-%m-%d") -> Dict[str, Union[bool, str, datetime]]:
        """
        Validate date string.
        
        Args:
            date_string (str): Date string to validate
            date_format (str): Expected date format
            
        Returns:
            dict: Validation result with datetime object
        """
        if not date_string or not isinstance(date_string, str):
            return {'valid': False, 'message': 'Date cannot be empty', 'date': None}
        
        try:
            date_obj = datetime.strptime(date_string.strip(), date_format)
            
            # Check if date is reasonable (not too far in past/future)
            current_year = datetime.now().year
            if date_obj.year < 1900 or date_obj.year > current_year + 10:
                return {'valid': False, 'message': 'Date is outside reasonable range', 'date': date_obj}
            
            return {'valid': True, 'message': 'Valid date', 'date': date_obj}
            
        except ValueError:
            return {'valid': False, 'message': f'Invalid date format. Expected: {date_format}', 'date': None}
    
    @staticmethod
    def validate_course_id(course_id: str) -> Dict[str, Union[bool, str]]:
        """
        Validate course ID format.
        
        Args:
            course_id (str): Course ID to validate
            
        Returns:
            dict: Validation result
        """
        if not course_id or not isinstance(course_id, str):
            return {'valid': False, 'message': 'Course ID cannot be empty'}
        
        course_id = course_id.strip().upper()
        
        # Course ID format: 3-4 letters followed by 3-4 numbers (e.g., CS101, MATH1001)
        if not re.match(r'^[A-Z]{2,4}\d{3,4}$', course_id):
            return {'valid': False, 'message': 'Course ID format: 2-4 letters followed by 3-4 numbers (e.g., CS101)'}
        
        return {'valid': True, 'message': 'Valid course ID', 'normalized': course_id}
    
    @staticmethod
    def validate_capacity(capacity: Union[str, int]) -> Dict[str, Union[bool, str, int]]:
        """
        Validate course capacity.
        
        Args:
            capacity: Capacity value to validate
            
        Returns:
            dict: Validation result with normalized value
        """
        try:
            capacity_int = int(capacity)
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Capacity must be a number', 'value': 0}
        
        if capacity_int < 1:
            return {'valid': False, 'message': 'Capacity must be at least 1', 'value': 1}
        
        if capacity_int > 500:  # Reasonable upper limit
            return {'valid': False, 'message': 'Capacity cannot exceed 500', 'value': 500}
        
        return {'valid': True, 'message': 'Valid capacity', 'value': capacity_int}
    
    @classmethod
    def validate_user_data(cls, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate complete user data dictionary.
        
        Args:
            user_data (dict): User data to validate
            
        Returns:
            dict: Validation results for all fields
        """
        results = {}
        
        # Required fields
        required_fields = ['username', 'password', 'name', 'email']
        
        for field in required_fields:
            if field not in user_data:
                results[field] = {'valid': False, 'message': f'{field} is required'}
                continue
            
            if field == 'username':
                results[field] = cls.validate_username(user_data[field])
            elif field == 'password':
                results[field] = cls.validate_password(user_data[field])
            elif field == 'name':
                results[field] = cls.validate_name(user_data[field])
            elif field == 'email':
                results[field] = {'valid': cls.validate_email(user_data[field]), 
                                'message': 'Valid email' if cls.validate_email(user_data[field]) else 'Invalid email'}
        
        # Optional fields
        if 'phone' in user_data:
            results['phone'] = cls.validate_phone(user_data['phone'])
        
        if 'salary' in user_data:
            results['salary'] = cls.validate_salary(user_data['salary'])
        
        # Overall validation
        all_valid = all(result.get('valid', False) for result in results.values())
        results['overall'] = {'valid': all_valid, 'message': 'All fields valid' if all_valid else 'Some fields have errors'}
        
        return results
