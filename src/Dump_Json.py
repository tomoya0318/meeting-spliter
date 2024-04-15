import json
from records import Attendance, GradeAttendance, Member
from spliter import update_attendance, check_same_half, select_half

class DumpJson:
    def __init__(self, json_file, absents):
        self.json_file = json_file
        self.grade_attendances = {
            "B4": GradeAttendance("B4"),
            "M1": GradeAttendance("M1"),
            "M2": GradeAttendance("M2")
        }
        self.absents = absents

    def dump_to_json(self):
        members = []
        done_members = []

        with open(self.json_file) as f:
            data = json.load(f)

        for item in data:
            member = Member(
                grade=item["grade"],
                name=item["name"],
                last=Attendance[item["last"]],
                previous=Attendance[item["previous"]]
            )
            
            grade = self.grade_attendances[member.grade]

            if member.mark_absent_if_needed(self.absents):
                grade.increment_member_num()
                next = check_same_half(member)

                if next != False:
                    update_attendance(member, grade, next)
                    done_members.append(member)
                else:
                    members.append(member)
            else:
                update_attendance(member, grade, Attendance.ABSENT)
                done_members.append(member)

        for member in members:
            grade = self.grade_attendances[member.grade]
            next = select_half(member, grade)
            update_attendance(member, grade, next)
            done_members.append(member)

        members_dict = [member.to_dict() for member in done_members]


        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(members_dict, f, ensure_ascii=False, indent=4)