"""
Base User class for the Portal System
Implements common functionality for all user types
"""

from abc import ABC, abstractmethod
import hashlib
import json
from datetime import datetime


class User(ABC):
    """
    Abstract base class for all user types in the portal system.
    Implements common functionality and defines interface for subclasses.
    """
    
    def __init__(self, username, password, name, email, user_id, first_login=False):
        """
        Initialize a User object.
        
        Args:
            username (str): Unique username for login
            password (str): User password (will be hashed)
            name (str): Full name of the user
            email (str): Email address
            user_id (str): Unique user identifier
            first_login (bool): Flag indicating if this is the user's first login
        """
        self._username = username
        self._password = self._hash_password(password)
        self._name = name
        self._email = email
        self._user_id = user_id
        self._last_login = None
        self._is_logged_in = False
        self._first_login = first_login
    
    def _hash_password(self, password):
        """
        Hash password using SHA-256 for security.
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_credentials(self, username, password):
        """
        Validate login credentials.
        
        Args:
            username (str): Username to validate
            password (str): Password to validate
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        return (self._username == username and 
                self._password == self._hash_password(password))
    
    def login(self, username, password):
        """
        Perform user login.
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        if self.validate_credentials(username, password):
            self._is_logged_in = True
            self._last_login = datetime.now()
            print(f"Welcome, {self._name}!")
            return True
        else:
            print("Invalid credentials. Please try again.")
            return False
    
    def logout(self):
        """Perform user logout."""
        if self._is_logged_in:
            print(f"Goodbye, {self._name}!")
            self._is_logged_in = False
            return True
        return False
    
    def change_password(self, old_password, new_password):
        """
        Change user password.
        
        Args:
            old_password (str): Current password
            new_password (str): New password
            
        Returns:
            bool: True if password changed successfully, False otherwise
        """
        if self._password == self._hash_password(old_password):
            self._password = self._hash_password(new_password)
            print("Password changed successfully!")
            return True
        else:
            print("Incorrect current password.")
            return False
    
    def change_username(self, new_username):
        """
        Change username.
        
        Args:
            new_username (str): New username to set
            
        Returns:
            bool: True if username changed successfully
        """
        self._username = new_username
        print("Username changed successfully!")
        return True
    
    def set_credentials(self, new_username, new_password):
        """
        Set new credentials for first-time users.
        
        Args:
            new_username (str): New username
            new_password (str): New password
            
        Returns:
            bool: True if credentials were updated
        """
        # Change username
        self._username = new_username
        
        # Change password (directly without verification)
        self._password = self._hash_password(new_password)
        
        # Mark first login complete
        self._first_login = False
        
        print("Your credentials have been updated successfully!")
        return True
    
    @abstractmethod
    def display_menu(self):
        """
        Abstract method to display role-specific menu.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def get_user_type(self):
        """
        Abstract method to return user type.
        Must be implemented by subclasses.
        """
        pass
    
    # Getter methods (public interface)
    @property
    def username(self):
        return self._username
    
    @property
    def name(self):
        return self._name
    
    @property
    def email(self):
        return self._email
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def is_logged_in(self):
        return self._is_logged_in
    
    @property
    def last_login(self):
        return self._last_login
        
    @property
    def first_login(self):
        return self._first_login
    
    @first_login.setter
    def first_login(self, value):
        self._first_login = value
    
    # Setter methods with validation
    @name.setter
    def name(self, new_name):
        if new_name and len(new_name.strip()) > 0:
            self._name = new_name.strip()
        else:
            raise ValueError("Name cannot be empty")
    
    @email.setter
    def email(self, new_email):
        # Basic email validation
        if "@" in new_email and "." in new_email:
            self._email = new_email
        else:
            raise ValueError("Invalid email format")
    
    def to_dict(self):
        """
        Convert user object to dictionary for serialization.
        
        Returns:
            dict: User data as dictionary
        """
        return {
            'username': self._username,
            'password': self._password,  # Already hashed
            'name': self._name,
            'email': self._email,
            'user_id': self._user_id,
            'user_type': self.get_user_type(),
            'last_login': self._last_login.isoformat() if self._last_login else None,
            'first_login': self._first_login
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create user object from dictionary.
        
        Args:
            data (dict): User data dictionary
            
        Returns:
            User: User object (specific subclass)
        """
        # This method will be overridden in subclasses
        pass
    
    def __str__(self):
        """String representation of user."""
        return f"{self.get_user_type()}: {self._name} ({self._username})"
    
    def __repr__(self):
        """Official string representation of user."""
        return f"{self.__class__.__name__}(username='{self._username}', name='{self._name}')"
