
"""
CSV Grade Analyzer
Purpose:
Reads a CSV file containing student names and grades,
then calculates summary statistics for reporting.
"""

import csv
from statistics import mean

def analyze_grades(file_path):
    grades = []

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    grades.append(float(row["Grade"]))
                except (ValueError, KeyError):
                    continue

        if not grades:
            print("No valid grades found.")
            return

        print("Grade Analysis Summary")
        print("----------------------")
        print(f"Number of records: {len(grades)}")
        print(f"Average grade: {mean(grades):.2f}")
        print(f"Highest grade: {max(grades):.2f}")
        print(f"Lowest grade: {min(grades):.2f}")

    except FileNotFoundError:
        print("Error: File not found.")
    except OSError as e:
        print(f"File access error: {e}")

if __name__ == "__main__":
    file_path = input("Enter the CSV file path: ").strip().strip('"')
    analyze_grades(file_path)
