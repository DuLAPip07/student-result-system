"""
student.py
Defines the Student class and the validation helpers for student details.
"""

import re
from datetime import datetime

# ---------------------------------------------------------------------------
# University settings
# ---------------------------------------------------------------------------

# College codes used in matriculation numbers.
COLLEGE_CODES = ("SCI", "ENG", "MHS", "SMS", "LAW", "PHM")

# Full college names. Only the codes you fill in here are shown as names;
# any code missing from this dictionary is displayed as the code itself.
COLLEGE_NAMES = {
    "SCI": "College of Sciences",
    # "ENG": "College of Engineering",   <- add the full names of the others
}

# Matriculation numbers look like 24/SCI01/131:
#   year (20-26) / college code + 2 digits / 3 or 4 digits
# The pattern is built from COLLEGE_CODES, so adding a college
# only means adding its code to the tuple above.
ID_PATTERN = re.compile(
    r"^2[0-6]/(" + "|".join(COLLEGE_CODES) + r")\d{2}/\d{3,4}$"
)

# Names may contain letters, spaces, hyphens and apostrophes only.
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z\s'\-]{1,59}$")

# Department names, e.g. "Computer Science", "Civil & Environmental Engineering".
DEPARTMENT_PATTERN = re.compile(r"^[A-Za-z][A-Za-z\s&'\-]{2,59}$")

# Course codes, e.g. CSC201, MTH101.
COURSE_CODE_PATTERN = re.compile(r"^[A-Z]{3}\d{3}$")

# Academic session, e.g. 2026/2027.
SESSION_PATTERN = re.compile(r"^(20\d{2})/(20\d{2})$")

LEVELS = (100, 200, 300, 400, 500, 600)
SEMESTERS = ("First", "Second")
VALID_GENDERS = ("Male", "Female")
DATE_FORMAT = "%Y-%m-%d"
MIN_AGE = 15   # youngest age accepted for a university student


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def is_valid_student_id(student_id):
    """Return True if the matriculation number matches the university format."""
    return bool(ID_PATTERN.match(student_id))


def get_college_code(student_id):
    """Pull the college code out of a matric number: 24/SCI01/131 -> SCI."""
    return student_id.split("/")[1][:3]


def get_college_name(student_id):
    """Return the college name (or its code if the name is not listed)."""
    code = get_college_code(student_id)
    return COLLEGE_NAMES.get(code, code)


def is_valid_name(name):
    """Return True if the name contains only allowed characters."""
    return bool(NAME_PATTERN.match(name))


def is_valid_department(department):
    """Return True if the department name looks sensible."""
    return bool(DEPARTMENT_PATTERN.match(department))


def parse_level(text):
    """
    Turn text such as '200' or '200L' into an int level.
    Returns None if it is not one of 100, 200, ..., 600.
    """
    text = text.strip().upper().rstrip("L")
    try:
        level = int(text)
    except ValueError:
        return None
    return level if level in LEVELS else None


def is_valid_course_code(code):
    """Return True for codes like CSC201."""
    return bool(COURSE_CODE_PATTERN.match(code))


def is_valid_session(session):
    """Return True for sessions like 2026/2027 (second year = first + 1)."""
    match = SESSION_PATTERN.match(session)
    if not match:
        return False
    return int(match.group(2)) == int(match.group(1)) + 1


def is_valid_dob(date_text):
    """Return True if the text is a real YYYY-MM-DD date and the student
    is at least MIN_AGE years old today."""
    try:
        born = datetime.strptime(date_text, DATE_FORMAT)
    except ValueError:
        return False
    today = datetime.now()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return MIN_AGE <= age <= 80


# ---------------------------------------------------------------------------
# Student class
# ---------------------------------------------------------------------------

class Student:
    """Represents one university student and their course results."""

    def __init__(self, student_id, name, department, level, gender,
                 date_of_birth, courses=None, session=None,
                 semester=None, result_date=None):
        self.student_id = student_id          # matric number
        self.name = name
        self.department = department
        self.level = level                    # 100 - 600
        self.gender = gender
        self.date_of_birth = date_of_birth
        # courses is a list of dictionaries, one per course:
        #   [{"code": "CSC201", "units": 3, "score": 72.0}, ...]
        self.courses = courses if courses is not None else []
        self.session = session                # e.g. "2026/2027"
        self.semester = semester              # "First" or "Second"
        # The date the result was last entered/updated (YYYY-MM-DD).
        self.result_date = result_date

    @property
    def college(self):
        """College name worked out from the matric number."""
        return get_college_name(self.student_id)

    def has_results(self):
        """True once course results have been recorded for this student."""
        return len(self.courses) > 0

    def set_results(self, courses, session, semester):
        """Store results and stamp today's date as the result date."""
        self.courses = courses
        self.session = session
        self.semester = semester
        self.result_date = datetime.now().strftime(DATE_FORMAT)

    def to_dict(self):
        """Convert the student to a plain dictionary (for saving as JSON)."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "level": self.level,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "courses": self.courses,
            "session": self.session,
            "semester": self.semester,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Student object from a dictionary loaded from JSON."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            department=data["department"],
            level=data["level"],
            gender=data["gender"],
            date_of_birth=data["date_of_birth"],
            courses=data.get("courses", []),
            session=data.get("session"),
            semester=data.get("semester"),
            result_date=data.get("result_date"),
        )

    def __str__(self):
        return (f"{self.student_id} | {self.name} | {self.department} | "
                f"{self.level}L | {self.gender} | DOB: {self.date_of_birth}")
