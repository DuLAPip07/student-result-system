# Student Result Management System

A menu-driven Python application that manages student records and
academic results for a university. Built for the **New Horizon
Introduction to Python Programming** project.

## Features

**Student management**
- Register, view, search (by matric number or name), update and delete students
- Each student has a matric number, full name, department, level (100-600),
  gender and date of birth, all validated
- The college is worked out automatically from the matric number

**Result management**
- Record results for 5 to 12 courses per student (course code, credit units, score)
- Academic session (e.g. 2026/2027) and semester are stored with the result
- Automatic total, average, per-course grade, GPA (5.0 scale) and overall grade
- Change a score or credit units, add a course, or remove a course
- Statement of result for each student; the date the result was entered is stored automatically

**Reporting and analysis**
- List all results with total, average, GPA and grade
- Sort by average, by GPA (highest to lowest) or by name (A-Z)
- Look at all levels together or one level at a time (100-600)
- Statistics: average score, average GPA, best and lowest average,
  highest and lowest single score, and average per course
- Save any statement of result or report to a text file

**Data persistence**
- All data is saved to `data/students.json` after every change
- Data is loaded when the program starts
- A missing or damaged data file is handled without crashing

## How to run

1. Install Python 3.8 or newer (check with `python --version`).
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

```
python main.py
```

No extra libraries are needed. Only the Python standard library is used.

## Project structure

```
student_result_system/
├── main.py        # Entry point and menu
├── student.py     # Student class and input validation (regex)
├── results.py     # Totals, averages, grading, GPA, sorting, statistics
├── storage.py     # Load and save data (JSON)
├── reports.py     # Statement of result and report generation
├── data/
│   └── students.json   # Created automatically on first save
└── README.md
```

Reports saved from the program go into a `reports/` folder, created automatically.

## Matriculation number format

Students are identified by their matriculation number, for example `24/SCI01/131`
(year / college code + 2 digits / 3 or 4 digits).

- Year: 20 to 26
- College codes: SCI, ENG, MHS, SMS, LAW, PHM

The format is checked with a regular expression in `student.py`.

## Grading scale

| Score  | Grade | Grade point | Remark    |
|--------|-------|-------------|-----------|
| 70-100 | A     | 5           | Excellent |
| 60-69  | B     | 4           | Very Good |
| 50-59  | C     | 3           | Good      |
| 45-49  | D     | 2           | Fair      |
| 40-44  | E     | 1           | Pass      |
| 0-39   | F     | 0           | Fail      |

GPA = sum of (grade point x credit units) / total credit units.
The overall grade is based on the student's average score.

## Python concepts used

| Concept | Where |
|---|---|
| Variables, data types, type conversion | `int()` and `float()` for levels, units and scores in `main.py` |
| if / elif / else, for, while | Menu loop and input validation in `main.py`, grading in `results.py` |
| Lists, tuples, dictionaries | Students in a dictionary; courses as a list of dictionaries; `GRADE_SCALE` as a list of tuples; `COLLEGE_CODES` as a tuple |
| Functions with parameters and return values | Every module |
| Sorting | `sorted()` with `key=lambda` in `results.py` |
| Exception handling | `try / except / else / finally` in `storage.py` and `ask_whole_number()` / `ask_score()` in `main.py` |
| File handling (JSON) | `storage.py`, `reports.py` |
| Modules and packages | Five separate `.py` files |
| Object-Oriented Programming | `Student` class in `student.py` (methods, `@property`, `@classmethod`) |
| Dates and times | `datetime` for result dates, age check on date of birth, report timestamps |
| Standard library | `os`, `json`, `re`, `datetime` |
| Regular expressions | Matric number, name, department, course code and session validation |
