from enum import Enum

from pydantic import BaseModel


class Attendance(str, Enum):
    BEFORE = "BEFORE"
    AFTER = "AFTER"
    ABSENT = "ABSENT"


class Grade(str, Enum):
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"
    M1 = "M1"
    M2 = "M2"


class Member(BaseModel):
    grade: Grade
    name: str
    last: Attendance
    previous: Attendance
    previous: Attendance
