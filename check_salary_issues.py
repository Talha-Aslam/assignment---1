#!/usr/bin/env python3
"""Check for salary calculation issues."""

from system_manager import SystemManager

def check_salary_issues():
    """Check for issues in salary information."""
    manager = SystemManager()
    
    teachers = manager.get_all_teachers()
    if not teachers:
        print("No teachers found")
        return
    
    print("SALARY INFORMATION ANALYSIS")
    print("="*50)
    
    for i, teacher in enumerate(teachers[:3]):  # Check first 3 teachers
        print(f"\n👤 Teacher {i+1}: {teacher.name} ({teacher.teacher_id})")
        print(f"💰 Base Salary: ${teacher.salary:,.2f}")
        print(f"📊 Number of Salary Slips: {len(teacher.salary_slips)}")
        
        # Check for duplicates
        months_seen = {}
        for slip in teacher.salary_slips:
            month_year = f"{slip.month} {slip.year}"
            if month_year in months_seen:
                months_seen[month_year] += 1
            else:
                months_seen[month_year] = 1
        
        print("📅 Months breakdown:")
        for month_year, count in months_seen.items():
            status = "⚠️ DUPLICATE" if count > 1 else "✅"
            print(f"   {month_year}: {count} slip(s) {status}")
        
        # Verify calculations for first slip
        if teacher.salary_slips:
            slip = teacher.salary_slips[0]
            print(f"\n🔍 Calculation Verification (Sample slip):")
            print(f"   Basic Salary: ${slip.basic_salary:,.2f}")
            
            # Recalculate allowances
            expected_housing = slip.basic_salary * 0.15
            expected_transport = 500.0
            expected_medical = 300.0
            total_allowances = expected_housing + expected_transport + expected_medical
            
            print(f"   Housing Allowance: ${slip.allowances.get('Housing Allowance', 0):,.2f}")
            print(f"   Expected Housing: ${expected_housing:,.2f}")
            
            # Recalculate deductions
            expected_tax = slip.basic_salary * 0.12
            expected_insurance = 150.0
            expected_pension = slip.basic_salary * 0.05
            total_deductions = expected_tax + expected_insurance + expected_pension
            
            print(f"   Tax: ${slip.deductions.get('Tax', 0):,.2f}")
            print(f"   Expected Tax: ${expected_tax:,.2f}")
            
            expected_net = slip.basic_salary + total_allowances - total_deductions
            print(f"   Net Salary: ${slip.net_salary:,.2f}")
            print(f"   Expected Net: ${expected_net:,.2f}")
            
            if abs(slip.net_salary - expected_net) > 0.01:
                print("   ❌ CALCULATION ERROR DETECTED!")
            else:
                print("   ✅ Calculations are correct")

if __name__ == "__main__":
    check_salary_issues()
