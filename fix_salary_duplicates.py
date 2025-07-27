#!/usr/bin/env python3
"""Fix duplicate salary slips issue."""

from system_manager import SystemManager

def fix_duplicate_salary_slips():
    """Remove duplicate salary slips and keep only unique month/year combinations."""
    manager = SystemManager()
    
    teachers = manager.get_all_teachers()
    if not teachers:
        print("No teachers found")
        return
    
    print("FIXING DUPLICATE SALARY SLIPS")
    print("="*50)
    
    total_duplicates_removed = 0
    
    for teacher in teachers:
        print(f"\n👤 Processing: {teacher.name} ({teacher.teacher_id})")
        print(f"   Original slips: {len(teacher.salary_slips)}")
        
        # Track unique month/year combinations
        unique_slips = {}
        duplicates_count = 0
        
        for slip in teacher.salary_slips:
            month_year_key = f"{slip.month}_{slip.year}"
            
            if month_year_key not in unique_slips:
                # First occurrence - keep it
                unique_slips[month_year_key] = slip
            else:
                # Duplicate - count it
                duplicates_count += 1
        
        # Replace salary_slips with unique ones only
        teacher.salary_slips = list(unique_slips.values())
        
        print(f"   Duplicates removed: {duplicates_count}")
        print(f"   Final slips: {len(teacher.salary_slips)}")
        
        # Show the months we kept
        months = [f"{slip.month} {slip.year}" for slip in teacher.salary_slips]
        print(f"   Months: {', '.join(months)}")
        
        total_duplicates_removed += duplicates_count
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total teachers processed: {len(teachers)}")
    print(f"   Total duplicates removed: {total_duplicates_removed}")
    
    # Save the cleaned data
    print("\n💾 Saving cleaned data...")
    manager.save_all_data()
    print("✅ Duplicate salary slips removed successfully!")
    
    # Verify the fix
    print("\n🔍 VERIFICATION:")
    first_teacher = teachers[0]
    print(f"   {first_teacher.name} now has {len(first_teacher.salary_slips)} salary slips")
    for slip in first_teacher.salary_slips:
        print(f"     • {slip.month} {slip.year}")

if __name__ == "__main__":
    fix_duplicate_salary_slips()
