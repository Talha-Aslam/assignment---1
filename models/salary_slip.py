"""
SalarySlip class for managing teacher salary information
"""

import json
from datetime import datetime


class SalarySlip:
    """
    Represents a salary slip for teachers.
    Manages salary components, calculations, and display.
    """
    
    def __init__(self, slip_id, teacher_id, month, year, basic_salary, 
                 allowances=None, deductions=None):
        """
        Initialize a SalarySlip object.
        
        Args:
            slip_id (str): Unique slip identifier
            teacher_id (str): Teacher ID
            month (str): Month name
            year (int): Year
            basic_salary (float): Basic salary amount
            allowances (dict): Dictionary of allowance types and amounts
            deductions (dict): Dictionary of deduction types and amounts
        """
        self.slip_id = slip_id
        self.teacher_id = teacher_id
        self.month = month
        self.year = year
        self.basic_salary = basic_salary
        self.allowances = allowances or {}
        self.deductions = deductions or {}
        self.generated_date = datetime.now()
        self.net_salary = self.calculate_net_salary()
    
    def calculate_net_salary(self):
        """
        Calculate net salary after allowances and deductions.
        
        Returns:
            float: Net salary amount
        """
        total_allowances = sum(self.allowances.values())
        total_deductions = sum(self.deductions.values())
        net = self.basic_salary + total_allowances - total_deductions
        return max(0, net)  # Ensure non-negative salary
    
    def add_allowance(self, allowance_type, amount):
        """
        Add an allowance to the salary slip.
        
        Args:
            allowance_type (str): Type of allowance
            amount (float): Allowance amount
        """
        self.allowances[allowance_type] = amount
        self.net_salary = self.calculate_net_salary()
    
    def add_deduction(self, deduction_type, amount):
        """
        Add a deduction to the salary slip.
        
        Args:
            deduction_type (str): Type of deduction
            amount (float): Deduction amount
        """
        self.deductions[deduction_type] = amount
        self.net_salary = self.calculate_net_salary()
    
    def remove_allowance(self, allowance_type):
        """
        Remove an allowance from the salary slip.
        
        Args:
            allowance_type (str): Type of allowance to remove
        """
        if allowance_type in self.allowances:
            del self.allowances[allowance_type]
            self.net_salary = self.calculate_net_salary()
            return True
        return False
    
    def remove_deduction(self, deduction_type):
        """
        Remove a deduction from the salary slip.
        
        Args:
            deduction_type (str): Type of deduction to remove
        """
        if deduction_type in self.deductions:
            del self.deductions[deduction_type]
            self.net_salary = self.calculate_net_salary()
            return True
        return False
    
    def display(self):
        """Display formatted salary slip."""
        print(f"\n{'='*50}")
        print(f"             SALARY SLIP")
        print(f"{'='*50}")
        print(f"Slip ID: {self.slip_id}")
        print(f"Teacher ID: {self.teacher_id}")
        print(f"Month/Year: {self.month} {self.year}")
        print(f"Generated: {self.generated_date.strftime('%Y-%m-%d')}")
        print(f"{'='*50}")
        
        print(f"\nEARNINGS:")
        print(f"{'Basic Salary':<20}: ${self.basic_salary:>10,.2f}")
        
        total_allowances = 0
        if self.allowances:
            for allowance_type, amount in self.allowances.items():
                print(f"{allowance_type:<20}: ${amount:>10,.2f}")
                total_allowances += amount
        
        print(f"{'Total Allowances':<20}: ${total_allowances:>10,.2f}")
        gross_salary = self.basic_salary + total_allowances
        print(f"{'Gross Salary':<20}: ${gross_salary:>10,.2f}")
        
        print(f"\nDEDUCTIONS:")
        total_deductions = 0
        if self.deductions:
            for deduction_type, amount in self.deductions.items():
                print(f"{deduction_type:<20}: ${amount:>10,.2f}")
                total_deductions += amount
        else:
            print("No deductions")
        
        print(f"{'Total Deductions':<20}: ${total_deductions:>10,.2f}")
        
        print(f"\n{'='*50}")
        print(f"{'NET SALARY':<20}: ${self.net_salary:>10,.2f}")
        print(f"{'='*50}")
    
    def get_summary(self):
        """
        Get salary slip summary.
        
        Returns:
            dict: Summary of salary components
        """
        return {
            'slip_id': self.slip_id,
            'month_year': f"{self.month} {self.year}",
            'basic_salary': self.basic_salary,
            'total_allowances': sum(self.allowances.values()),
            'total_deductions': sum(self.deductions.values()),
            'net_salary': self.net_salary
        }
    
    def save_to_file(self, filename):
        """
        Save salary slip to file.
        
        Args:
            filename (str): File path to save to
        """
        try:
            with open(filename, 'w') as file:
                json.dump(self.to_dict(), file, indent=2)
            print(f"Salary slip saved to {filename}")
        except Exception as e:
            print(f"Error saving salary slip: {e}")
    
    def to_dict(self):
        """
        Convert salary slip to dictionary.
        
        Returns:
            dict: Salary slip data as dictionary
        """
        return {
            'slip_id': self.slip_id,
            'teacher_id': self.teacher_id,
            'month': self.month,
            'year': self.year,
            'basic_salary': self.basic_salary,
            'allowances': self.allowances,
            'deductions': self.deductions,
            'net_salary': self.net_salary,
            'generated_date': self.generated_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create salary slip from dictionary.
        
        Args:
            data (dict): Salary slip data
            
        Returns:
            SalarySlip: SalarySlip object
        """
        slip = cls(
            data['slip_id'],
            data['teacher_id'],
            data['month'],
            data['year'],
            data['basic_salary'],
            data.get('allowances', {}),
            data.get('deductions', {})
        )
        
        if 'generated_date' in data:
            slip.generated_date = datetime.fromisoformat(data['generated_date'])
        
        return slip
    
    def __str__(self):
        """String representation of salary slip."""
        return f"Salary Slip {self.slip_id} - {self.month} {self.year} (${self.net_salary:,.2f})"
    
    def __repr__(self):
        """Official string representation."""
        return f"SalarySlip(slip_id='{self.slip_id}', teacher_id='{self.teacher_id}', month='{self.month}')"
    
    def __eq__(self, other):
        """Check equality based on slip_id."""
        if isinstance(other, SalarySlip):
            return self.slip_id == other.slip_id
        return False
    
    def __lt__(self, other):
        """Compare salary slips by date."""
        if isinstance(other, SalarySlip):
            return (self.year, self.month) < (other.year, other.month)
        return NotImplemented
