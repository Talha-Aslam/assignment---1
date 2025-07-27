#!/usr/bin/env python3
"""Generate sample salary slips for teachers."""

from system_manager import SystemManager
from models.salary_slip import SalarySlip
import random

def generate_sample_salary_slips():
    """Generate sample salary slips for all teachers."""
    manager = SystemManager()
    
    teachers = manager.get_all_teachers()
    if not teachers:
        print("No teachers found")
        return
    
    months = ["January", "February", "March", "April", "May", "June"]
    year = 2025
    
    print(f"Generating salary slips for {len(teachers)} teachers...")
    
    for teacher in teachers:
        print(f"Creating salary slips for {teacher.name} ({teacher.teacher_id})")
        
        # Check existing salary slips to avoid duplicates
        existing_months = set()
        for existing_slip in teacher.salary_slips:
            month_year_key = f"{existing_slip.month}_{existing_slip.year}"
            existing_months.add(month_year_key)
        
        # Generate 3-4 salary slips per teacher (only if they don't exist)
        for i, month in enumerate(months[:4]):
            month_year_key = f"{month}_{year}"
            
            # Skip if this month already exists
            if month_year_key in existing_months:
                print(f"  Skipping {month} {year} - already exists")
                continue
            
            slip_id = f"SS{year}{i+1:02d}{teacher.teacher_id}"
            
            # Calculate allowances and deductions
            allowances = {
                "Housing Allowance": teacher.salary * 0.15,
                "Transport Allowance": 500.0,
                "Medical Allowance": 300.0
            }
            
            deductions = {
                "Tax": teacher.salary * 0.12,
                "Insurance": 150.0,
                "Pension": teacher.salary * 0.05
            }
            
            # Create salary slip
            salary_slip = SalarySlip(
                slip_id=slip_id,
                teacher_id=teacher.teacher_id,
                month=month,
                year=year,
                basic_salary=teacher.salary,
                allowances=allowances,
                deductions=deductions
            )
            
            # Add to teacher
            teacher.add_salary_slip(salary_slip)
    
    # Save the updated data
    print("Saving updated teacher data...")
    manager.save_all_data()
    print("Sample salary slips generated successfully!")
    
    # Test display for first teacher
    if teachers:
        print("\nSample salary slip display:")
        print("="*60)
        teachers[0].view_salary()

if __name__ == "__main__":
    generate_sample_salary_slips()
