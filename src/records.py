from dataclasses import dataclass
from enum import Enum

class Attendance(Enum):
    BEFORE = 'BEFORE'
    AFTER = 'AFTER'
    ABSENT = 'ABSENT'
    NULL = "NULL"

@dataclass
class Member:
    grade: str
    name: str
    last: Attendance
    previous: Attendance

    def grade_weight(self):
        grade_order = {"B4": 1, "M1": 2, "M2": 3}
        return grade_order.get(self.grade, 999)
    
    def mark_absent_if_needed(self, absents):
        flag = True
        if self.name in absents:
            flag = False
        return flag

    def update(self, next):
        self.previous = self.last
        self.last = next
    
    def to_dict(self):
        return {
            "grade": self.grade,
            "name": self.name,
            "last": self.last.value,
            "previous": self.previous.value
        }

@dataclass
class GradeAttendance:
    grade: str
    member_num: int = 0
    before_count: int = 0
    after_count: int = 0

    def increment_before_half(self):
        self.before_count += 1

    def increment_after_half(self):
        self.after_count += 1

    def increment_member_num(self):
        self.member_num += 1

    def compare(self):
        border = self.member_num // 2
        if self.after_count >= border:
            return Attendance.BEFORE
        elif self.before_count >= border:
            return Attendance.AFTER
        else:
            return None
                
