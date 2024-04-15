import random
from records import Attendance, Member, GradeAttendance

def update_attendance(member: Member, grade: GradeAttendance, next):
    if next == Attendance.BEFORE:
        grade.increment_before_half()
    elif next == Attendance.AFTER:
        grade.increment_after_half()
    member.update(next)

def check_same_half(member: Member):
    if member.last == member.previous == Attendance.BEFORE:
        return Attendance.AFTER
    elif member.last == member.previous == Attendance.AFTER:
        return Attendance.BEFORE
    else:
        return False

def select_half(member: Member, grade: GradeAttendance):
    choice = [Attendance.BEFORE, Attendance.AFTER]

    if not grade.compare():
        rand = random.randint(0, 1)
        return choice[rand]
    
    else:
        return grade.compare()
