"""
storage.py
Loads and saves student data to a JSON file.
"""

import json
import os

from student import Student

# Build the path from this file's location so the program works
# no matter which folder it is launched from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")


def load_students(path=DATA_FILE):
    """
    Load students from the JSON file and return a dictionary
    {student_id: Student}. If the file does not exist yet, or is
    damaged, return an empty dictionary instead of crashing.
    """
    students = {}
    file = None
    try:
        file = open(path, "r", encoding="utf-8")
        records = json.load(file)
    except FileNotFoundError:
        print("No saved data found. Starting with an empty system.")
    except json.JSONDecodeError:
        print("Warning: the data file is damaged. Starting with an empty system.")
    else:
        # Runs only when loading worked with no error.
        for record in records:
            try:
                student = Student.from_dict(record)
                students[student.student_id] = student
            except KeyError:
                print("Skipped one incomplete record in the data file.")
        print(f"Loaded {len(students)} student record(s).")
    finally:
        # Always runs, error or not: make sure the file is closed.
        if file is not None:
            file.close()
    return students


def save_students(students, path=DATA_FILE):
    """Save all students to the JSON file. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        records = [student.to_dict() for student in students.values()]
        with open(path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
    except OSError as error:
        print(f"Error: could not save data ({error}).")
        return False
    return True
