#!/usr/bin/env python3
"""
Quick script to display the course sections structure
"""
import json
from collections import defaultdict

# Load courses data
with open('data/courses.json', 'r') as f:
    courses_data = json.load(f)

# Group by course ID
courses = defaultdict(list)
for course in courses_data:
    section_info = f"Section {course['section']} - {course['instructor']} (Capacity: {course['capacity']}, Enrolled: {len(course['enrolled_students'])})"
    courses[course['course_id']].append(section_info)

# Display results
print("="*80)
print("COURSE SECTIONS OVERVIEW")
print("="*80)

for course_id, sections in courses.items():
    # Get course name from first section
    course_name = next(c['course_name'] for c in courses_data if c['course_id'] == course_id)
    print(f"\n📚 {course_id}: {course_name}")
    print("-" * 60)
    for section in sections:
        print(f"  {section}")

print(f"\n📊 SUMMARY:")
print(f"Total course types: {len(courses)}")
print(f"Total course sections: {len(courses_data)}")
print(f"Average sections per course: {len(courses_data)/len(courses):.1f}")
