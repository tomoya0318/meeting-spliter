import json
from Dump_Json import DumpJson
from records import Member, Attendance
def main():

    before = []
    after = []
    absent = []
    json_file = "../data/member.json"
    DJ = DumpJson(json_file, absent)
    DJ.dump_to_json()
    
    with open(json_file) as f:
        data = json.load(f)
    
    members = []
    for item in data:
        member = Member(
            grade=item["grade"],
            name=item["name"],
            last=Attendance[item["last"]],
            previous=Attendance[item["previous"]]
        )
        members.append(member)

    members.sort(key=lambda x: (x.grade_weight(), x.name))
    before = [m.name for m in members if m.last == Attendance.BEFORE]
    after = [m.name for m in members if m.last == Attendance.AFTER]

    before_str = ", ".join(before)
    after_str = ", ".join(after)
    absent_str = ", ".join(absent)

    print(
        f"本日は研究ミーティングです\n\
前半: {before_str}\n\
後半: {after_str}\n\
欠席: {absent_str}"
    )
        
if __name__ == "__main__":
    main()