"""
main.py
Entry point: menu-driven interface for the Student Result Management System.
Run with:  python main.py
"""

import reports
import results
import storage
from student import (Student, is_valid_course_code, is_valid_department,
                     is_valid_dob, is_valid_name, is_valid_session,
                     is_valid_student_id, parse_level, SEMESTERS)


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def ask(prompt_text):
    """Read a line of input and remove extra spaces."""
    return input(prompt_text).strip()


def ask_student_id(students, must_exist):
    """
    Ask for a matric number until a valid one is given.
    must_exist=True  -> it must already be registered (update/delete/etc.)
    must_exist=False -> it must be new (adding a student)
    Returns None if the user types 'back'.
    """
    while True:
        student_id = ask("Matric number (e.g. 24/SCI01/131, or 'back'): ").upper()
        if student_id == "BACK":
            return None
        if not is_valid_student_id(student_id):
            print("Invalid matric number. Use the format 24/SCI01/131 "
                  "(year 20-26; college SCI, ENG, MHS, SMS, LAW or PHM).")
        elif must_exist and student_id not in students:
            print("No student with that matric number.")
        elif not must_exist and student_id in students:
            print("That matric number is already registered.")
        else:
            return student_id


def ask_name(current=None):
    """Ask for a full name. Pressing Enter keeps the current value."""
    while True:
        hint = f" [{current}]" if current else ""
        name = ask(f"Full name{hint}: ")
        if name == "" and current:
            return current
        if is_valid_name(name):
            return name.title()
        print("Invalid name. Use letters, spaces, hyphens or apostrophes only.")


def ask_department(current=None):
    """Ask for the department. Pressing Enter keeps the current value."""
    while True:
        hint = f" [{current}]" if current else ""
        department = ask(f"Department (e.g. Computer Science){hint}: ")
        if department == "" and current:
            return current
        if is_valid_department(department):
            return department.title()
        print("Invalid department. Use letters, spaces, '&' or hyphens only.")


def ask_level(current=None):
    """Ask for the level (100-600). Pressing Enter keeps the current value."""
    while True:
        hint = f" [{current}]" if current else ""
        text = ask(f"Level (100, 200, 300, 400, 500 or 600){hint}: ")
        if text == "" and current:
            return current
        level = parse_level(text)
        if level is not None:
            return level
        print("Invalid level. Enter 100, 200, 300, 400, 500 or 600.")


def ask_gender(current=None):
    """Ask for gender (Male/Female). Enter keeps the current value."""
    while True:
        hint = f" [{current}]" if current else ""
        answer = ask(f"Gender (M/F){hint}: ").upper()
        if answer == "" and current:
            return current
        if answer in ("M", "MALE"):
            return "Male"
        if answer in ("F", "FEMALE"):
            return "Female"
        print("Please enter M for Male or F for Female.")


def ask_dob(current=None):
    """Ask for date of birth (YYYY-MM-DD). Enter keeps the current value."""
    while True:
        hint = f" [{current}]" if current else ""
        dob = ask(f"Date of birth (YYYY-MM-DD){hint}: ")
        if dob == "" and current:
            return current
        if is_valid_dob(dob):
            return dob
        print("Invalid date. Use YYYY-MM-DD for a real date "
              "(the student must be at least 15 years old).")


def ask_session(current=None):
    """Ask for the academic session, e.g. 2026/2027."""
    while True:
        hint = f" [{current}]" if current else ""
        session = ask(f"Academic session (e.g. 2026/2027){hint}: ")
        if session == "" and current:
            return current
        if is_valid_session(session):
            return session
        print("Invalid session. Use two consecutive years, e.g. 2026/2027.")


def ask_semester(current=None):
    """Ask for the semester (First or Second)."""
    while True:
        hint = f" [{current}]" if current else ""
        answer = ask(f"Semester (1 = First, 2 = Second){hint}: ")
        if answer == "" and current:
            return current
        if answer in ("1", "2"):
            return SEMESTERS[int(answer) - 1]
        print("Enter 1 for First semester or 2 for Second semester.")


def ask_whole_number(prompt_text, low, high, current=None):
    """
    Ask for a whole number between low and high.
    Uses try/except to catch text that is not a number.
    """
    while True:
        hint = f" [{current}]" if current is not None else ""
        text = ask(f"{prompt_text}{hint}: ")
        if text == "" and current is not None:
            return current
        try:
            number = int(text)
        except ValueError:
            print("Please enter a whole number.")
        else:
            if low <= number <= high:
                return number
            print(f"The number must be between {low} and {high}.")


def ask_score(label, current=None):
    """
    Ask for a score between 0 and 100.
    Uses try/except to catch text that is not a number.
    """
    while True:
        hint = f" [{current}]" if current is not None else ""
        text = ask(f"  {label} score (0-100){hint}: ")
        if text == "" and current is not None:
            return current
        try:
            score = float(text)
        except ValueError:
            print("  Please enter a number, e.g. 72 or 65.5.")
        else:
            if 0 <= score <= 100:
                return score
            print("  Score must be between 0 and 100.")


def ask_course_code(taken_codes):
    """Ask for a new course code (e.g. CSC201) that is not already used."""
    while True:
        code = ask("  Course code (e.g. CSC201): ").upper().replace(" ", "")
        if not is_valid_course_code(code):
            print("  Invalid code. Use 3 letters followed by 3 digits, e.g. CSC201.")
        elif code in taken_codes:
            print("  That course is already entered.")
        else:
            return code


def ask_new_course(taken_codes):
    """Collect one course (code, credit units, score) and return it as a dict."""
    code = ask_course_code(taken_codes)
    units = ask_whole_number("  Credit units", results.MIN_UNITS, results.MAX_UNITS)
    score = ask_score(code)
    return {"code": code, "units": units, "score": score}


def choose_students_by_level(students):
    """
    Ask which level to look at. Enter = all levels.
    Returns (list of students, label for the report heading).
    """
    while True:
        text = ask("Filter by level (100-600), or press Enter for all levels: ")
        if text == "":
            return list(students.values()), "All levels"
        level = parse_level(text)
        if level is not None:
            chosen = results.students_in_level(students.values(), level)
            return chosen, f"{level} Level"
        print("Invalid level. Enter 100, 200, 300, 400, 500 or 600.")


def find_students(students, query):
    """Return students whose matric number matches exactly or whose name contains the query."""
    query = query.lower()
    return [s for s in students.values()
            if s.student_id.lower() == query or query in s.name.lower()]


def pause():
    ask("\nPress Enter to continue...")


# ---------------------------------------------------------------------------
# Student management (Section A)
# ---------------------------------------------------------------------------

def add_student(students):
    print("\n--- REGISTER NEW STUDENT ---")
    student_id = ask_student_id(students, must_exist=False)
    if student_id is None:
        return
    student = Student(student_id, ask_name(), ask_department(), ask_level(),
                      ask_gender(), ask_dob())
    students[student_id] = student
    storage.save_students(students)
    print(f"\n{student.name} ({student_id}) registered successfully "
          f"in {student.college}.")


def view_all_students(students):
    print("\n--- ALL REGISTERED STUDENTS ---")
    if not students:
        print("No students registered yet.")
        return
    print(f"{'Matric No.':<15}{'Name':<24}{'Department':<22}{'Level':<7}{'Gender':<8}")
    print("-" * 76)
    for student in results.sort_by_name(list(students.values())):
        print(f"{student.student_id:<15}{student.name[:22]:<24}"
              f"{student.department[:20]:<22}{student.level:<7}{student.gender:<8}")
    print(f"\nTotal students: {len(students)}")


def search_student(students):
    print("\n--- SEARCH FOR A STUDENT ---")
    query = ask("Enter matric number or part of the name: ")
    if not query:
        print("Nothing entered.")
        return
    matches = find_students(students, query)
    if not matches:
        print("No matching student found.")
        return
    print(f"\n{len(matches)} match(es) found:")
    for student in matches:
        print("  " + str(student))


def update_student(students):
    print("\n--- UPDATE STUDENT INFORMATION ---")
    student_id = ask_student_id(students, must_exist=True)
    if student_id is None:
        return
    student = students[student_id]
    print("Press Enter to keep the current value.")
    student.name = ask_name(student.name)
    student.department = ask_department(student.department)
    student.level = ask_level(student.level)
    student.gender = ask_gender(student.gender)
    student.date_of_birth = ask_dob(student.date_of_birth)
    storage.save_students(students)
    print("\nStudent information updated.")


def delete_student(students):
    print("\n--- DELETE A STUDENT RECORD ---")
    student_id = ask_student_id(students, must_exist=True)
    if student_id is None:
        return
    student = students[student_id]
    confirm = ask(f"Delete {student.name} permanently? (yes/no): ").lower()
    if confirm == "yes":
        del students[student_id]
        storage.save_students(students)
        print("Student record deleted.")
    else:
        print("Deletion cancelled.")


# ---------------------------------------------------------------------------
# Result management (Section B)
# ---------------------------------------------------------------------------

def record_results(students):
    print("\n--- RECORD RESULTS ---")
    student_id = ask_student_id(students, must_exist=True)
    if student_id is None:
        return
    student = students[student_id]
    if student.has_results():
        print("This student already has results. Use 'Update results' instead.")
        return

    session = ask_session()
    semester = ask_semester()
    count = ask_whole_number(
        f"Number of courses ({results.MIN_COURSES}-{results.MAX_COURSES})",
        results.MIN_COURSES, results.MAX_COURSES)

    courses = []
    for number in range(1, count + 1):
        print(f"Course {number} of {count}:")
        courses.append(ask_new_course({c["code"] for c in courses}))

    student.set_results(courses, session, semester)
    storage.save_students(students)
    average = results.calculate_average(courses)
    gpa = results.calculate_gpa(courses)
    grade, remark = results.assign_grade(average)
    print(f"\nResults saved. Average: {average:.2f} | GPA: {gpa:.2f} | "
          f"Grade: {grade} ({remark})")


def update_results(students):
    print("\n--- UPDATE RESULTS ---")
    student_id = ask_student_id(students, must_exist=True)
    if student_id is None:
        return
    student = students[student_id]
    if not student.has_results():
        print("No results recorded yet. Use 'Record results' first.")
        return

    courses = [dict(course) for course in student.courses]   # work on a copy
    while True:
        print("\n" + reports.build_course_table(courses))
        print("\n 1. Change a score   2. Change credit units   3. Add a course")
        print(" 4. Remove a course  0. Save and finish")
        choice = ask("Choose: ")

        if choice == "0":
            student.set_results(courses, student.session, student.semester)
            storage.save_students(students)
            print("\nResults updated.")
            return
        if choice in ("1", "2", "4"):
            code = ask("Course code: ").upper().replace(" ", "")
            course = next((c for c in courses if c["code"] == code), None)
            if course is None:
                print("That course is not in this student's results.")
            elif choice == "1":
                course["score"] = ask_score(code, course["score"])
            elif choice == "2":
                course["units"] = ask_whole_number(
                    "Credit units", results.MIN_UNITS, results.MAX_UNITS,
                    course["units"])
            elif len(courses) <= results.MIN_COURSES:
                print(f"A student must keep at least {results.MIN_COURSES} courses.")
            else:
                courses.remove(course)
        elif choice == "3":
            if len(courses) >= results.MAX_COURSES:
                print(f"No more than {results.MAX_COURSES} courses are allowed.")
            else:
                courses.append(ask_new_course({c["code"] for c in courses}))
        else:
            print("Invalid choice.")


def show_report_card(students):
    print("\n--- STATEMENT OF RESULT ---")
    student_id = ask_student_id(students, must_exist=True)
    if student_id is None:
        return
    student = students[student_id]
    card = reports.build_report_card(student)
    print("\n" + card)
    if student.has_results():
        if ask("\nSave this statement of result to a file? (yes/no): ").lower() == "yes":
            # File names cannot contain '/', so swap it for '-'.
            prefix = "result_" + student_id.replace("/", "-")
            path = reports.save_report(card, prefix=prefix)
            if path:
                print(f"Saved to: {path}")


# ---------------------------------------------------------------------------
# Reporting and analysis (Section C)
# ---------------------------------------------------------------------------

def list_results(students):
    print("\n--- ALL RESULTS ---")
    chosen, label = choose_students_by_level(students)
    scored = results.students_with_results(chosen)
    if not scored:
        print(f"No results have been recorded for: {label}.")
        return
    print("Sort by:  1) Average (highest to lowest)   2) GPA (highest to lowest)"
          "   3) Name (A-Z)")
    choice = ask("Choose 1, 2 or 3: ")
    if choice == "2":
        ordered = results.sort_by_gpa(scored)
    elif choice == "3":
        ordered = results.sort_by_name(scored)
    else:
        ordered = results.sort_by_average(scored)
    print(f"\n{label}\n")
    print(reports.build_results_table(ordered))


def show_class_statistics(students):
    print("\n--- STATISTICS ---")
    chosen, label = choose_students_by_level(students)
    print(reports.build_class_report(chosen, label))


def save_class_report(students):
    print("\n--- SAVE RESULT REPORT TO FILE ---")
    chosen, label = choose_students_by_level(students)
    text = reports.build_class_report(chosen, label)
    prefix = "result_report_" + label.replace(" ", "_")
    path = reports.save_report(text, prefix=prefix)
    if path:
        print(f"Report saved to: {path}")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

MENU = """
==============================================
   NEW HORIZON - STUDENT RESULT MANAGEMENT
==============================================
 STUDENTS
  1. Register new student
  2. View all students
  3. Search for a student
  4. Update student information
  5. Delete a student record
 RESULTS
  6. Record results
  7. Update results
  8. Show statement of result
 REPORTS
  9. List all results (sorted)
 10. Statistics (all levels or one level)
 11. Save result report to file
  0. Exit
----------------------------------------------"""


def main():
    students = storage.load_students()

    # Dictionary mapping each menu choice to the function that handles it.
    actions = {
        "1": add_student,
        "2": view_all_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": record_results,
        "7": update_results,
        "8": show_report_card,
        "9": list_results,
        "10": show_class_statistics,
        "11": save_class_report,
    }

    while True:
        print(MENU)
        choice = ask("Enter your choice: ")
        if choice == "0":
            storage.save_students(students)
            print("Data saved. Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please pick a number from the menu.")
            continue
        try:
            action(students)
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
        pause()


if __name__ == "__main__":
    main()
