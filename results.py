"""
results.py
Score calculation, grading, GPA, sorting and statistics.
"""

MIN_COURSES = 5     # every student must be scored in at least five courses
MAX_COURSES = 12
MIN_UNITS = 1
MAX_UNITS = 6

# Grade scale, checked from the highest down:
# (minimum score, letter, grade point, remark)
GRADE_SCALE = [
    (70, "A", 5, "Excellent"),
    (60, "B", 4, "Very Good"),
    (50, "C", 3, "Good"),
    (45, "D", 2, "Fair"),
    (40, "E", 1, "Pass"),
    (0, "F", 0, "Fail"),
]


def grade_for_score(score):
    """Return (letter, grade point, remark) for a score out of 100."""
    for minimum, letter, points, remark in GRADE_SCALE:
        if score >= minimum:
            return letter, points, remark
    return "F", 0, "Fail"


def calculate_total(courses):
    """Sum of all course scores."""
    return sum(course["score"] for course in courses)


def calculate_average(courses):
    """Average course score (0 if there are no courses)."""
    if not courses:
        return 0.0
    return calculate_total(courses) / len(courses)


def calculate_total_units(courses):
    """Total credit units registered."""
    return sum(course["units"] for course in courses)


def calculate_gpa(courses):
    """
    Grade Point Average on a 5.0 scale:
    sum(grade point x credit units) / sum(credit units).
    """
    total_units = calculate_total_units(courses)
    if total_units == 0:
        return 0.0
    quality_points = 0
    for course in courses:
        _, points, _ = grade_for_score(course["score"])
        quality_points += points * course["units"]
    return quality_points / total_units


def assign_grade(average):
    """Return (letter, remark) for an average score."""
    letter, _, remark = grade_for_score(average)
    return letter, remark


def students_with_results(students):
    """Keep only students whose results have been recorded."""
    return [s for s in students if s.has_results()]


def students_in_level(students, level):
    """Keep only students in the given level (e.g. 200)."""
    return [s for s in students if s.level == level]


def sort_by_average(students, highest_first=True):
    """Sort students by average score (highest to lowest by default)."""
    return sorted(students,
                  key=lambda s: calculate_average(s.courses),
                  reverse=highest_first)


def sort_by_gpa(students, highest_first=True):
    """Sort students by GPA (highest to lowest by default)."""
    return sorted(students,
                  key=lambda s: calculate_gpa(s.courses),
                  reverse=highest_first)


def sort_by_name(students):
    """Sort students alphabetically by name (ignoring upper/lower case)."""
    return sorted(students, key=lambda s: s.name.lower())


def class_statistics(students):
    """
    Work out statistics for the given students (only those with results).
    Returns a dictionary, or None if nobody has results yet.
    """
    scored = students_with_results(students)
    if not scored:
        return None

    averages = [calculate_average(s.courses) for s in scored]
    gpas = [calculate_gpa(s.courses) for s in scored]
    top_student = max(scored, key=lambda s: calculate_average(s.courses))
    bottom_student = min(scored, key=lambda s: calculate_average(s.courses))

    # Highest and lowest single course score, and the average per course code.
    highest = (-1, None, None)    # (score, student name, course code)
    lowest = (101, None, None)
    scores_by_course = {}
    for student in scored:
        for course in student.courses:
            score, code = course["score"], course["code"]
            if score > highest[0]:
                highest = (score, student.name, code)
            if score < lowest[0]:
                lowest = (score, student.name, code)
            scores_by_course.setdefault(code, []).append(score)

    course_averages = {code: (sum(marks) / len(marks), len(marks))
                       for code, marks in sorted(scores_by_course.items())}

    return {
        "number_scored": len(scored),
        "class_average": sum(averages) / len(averages),
        "class_gpa": sum(gpas) / len(gpas),
        "top_student": top_student,
        "top_average": max(averages),
        "bottom_student": bottom_student,
        "bottom_average": min(averages),
        "highest_score": highest,
        "lowest_score": lowest,
        "course_averages": course_averages,   # {code: (average, how many students)}
    }
