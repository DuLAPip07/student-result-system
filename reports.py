"""
reports.py
Builds text reports (statement of result, level report) and saves them.
"""

import os
from datetime import datetime

import results
from storage import BASE_DIR

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
WIDTH = 72
LINE = "=" * WIDTH
THIN = "-" * WIDTH


def build_course_table(courses):
    """Return the list of courses with units, score, grade and grade point."""
    lines = [f"{'Course Code':<16}{'Units':>7}{'Score':>10}{'Grade':>9}{'GP':>6}",
             THIN]
    for course in courses:
        letter, points, _ = results.grade_for_score(course["score"])
        lines.append(f"{course['code']:<16}{course['units']:>7}"
                     f"{course['score']:>10.1f}{letter:>9}{points:>6}")
    return "\n".join(lines)


def build_report_card(student):
    """Return an individual statement of result as a string."""
    lines = [LINE, "STATEMENT OF RESULT".center(WIDTH), LINE,
             f"Matric No     : {student.student_id}",
             f"Name          : {student.name}",
             f"College       : {student.college}",
             f"Department    : {student.department}",
             f"Level         : {student.level}",
             f"Gender        : {student.gender}",
             f"Date of Birth : {student.date_of_birth}"]

    if not student.has_results():
        lines += [THIN, "No results have been recorded for this student yet.", LINE]
        return "\n".join(lines)

    total = results.calculate_total(student.courses)
    average = results.calculate_average(student.courses)
    units = results.calculate_total_units(student.courses)
    gpa = results.calculate_gpa(student.courses)
    grade, remark = results.assign_grade(average)

    lines += [f"Session       : {student.session} ({student.semester} Semester)",
              THIN,
              build_course_table(student.courses),
              THIN,
              f"{'Total score':<30}{total:>10.1f}",
              f"{'Average score':<30}{average:>10.2f}",
              f"{'Total credit units':<30}{units:>10}",
              f"{'GPA (5.0 scale)':<30}{gpa:>10.2f}",
              f"{'Overall grade (by average)':<30}{grade:>10}  ({remark})",
              f"Result entered on: {student.result_date}",
              LINE]
    return "\n".join(lines)


def build_results_table(students):
    """Return a table of students with total, average, GPA and grade."""
    lines = [f"{'Pos':<5}{'Matric No.':<15}{'Name':<24}{'Level':>6}"
             f"{'Total':>8}{'Avg':>8}{'GPA':>6}{'Grd':>5}",
             THIN]
    for position, student in enumerate(students, start=1):
        total = results.calculate_total(student.courses)
        average = results.calculate_average(student.courses)
        gpa = results.calculate_gpa(student.courses)
        grade, _ = results.assign_grade(average)
        lines.append(f"{position:<5}{student.student_id:<15}{student.name[:22]:<24}"
                     f"{student.level:>6}{total:>8.1f}{average:>8.2f}"
                     f"{gpa:>6.2f}{grade:>5}")
    return "\n".join(lines)


def build_class_report(students, label="All levels"):
    """Return the full result report (ranked table + statistics)."""
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [LINE, "RESULT SUMMARY REPORT".center(WIDTH),
             label.center(WIDTH), f"Generated: {generated}".center(WIDTH), LINE]

    stats = results.class_statistics(students)
    if stats is None:
        lines.append("No results have been recorded yet.")
        return "\n".join(lines)

    ranked = results.sort_by_average(results.students_with_results(students))
    lines.append(build_results_table(ranked))
    lines.append(THIN)

    top, bottom = stats["top_student"], stats["bottom_student"]
    high_score, high_name, high_code = stats["highest_score"]
    low_score, low_name, low_code = stats["lowest_score"]

    lines += [
        "STATISTICS",
        f"Students with results : {stats['number_scored']}",
        f"Average score         : {stats['class_average']:.2f}",
        f"Average GPA           : {stats['class_gpa']:.2f}",
        f"Best average          : {stats['top_average']:.2f} ({top.name})",
        f"Lowest average        : {stats['bottom_average']:.2f} ({bottom.name})",
        f"Highest single score  : {high_score:.1f} - {high_name} ({high_code})",
        f"Lowest single score   : {low_score:.1f} - {low_name} ({low_code})",
        THIN,
        f"{'AVERAGE PER COURSE':<30}{'Students':>10}{'Average':>10}",
    ]
    for code, (average, count) in stats["course_averages"].items():
        lines.append(f"{code:<30}{count:>10}{average:>10.2f}")
    lines.append(LINE)
    return "\n".join(lines)


def save_report(text, prefix="result_report"):
    """Save report text into the reports folder. Returns the file path."""
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(REPORTS_DIR, f"{prefix}_{stamp}.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
    except OSError as error:
        print(f"Error: could not save the report ({error}).")
        return None
    return path
