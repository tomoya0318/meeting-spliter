import json
import sys
from pathlib import Path

from classifer import ClassifyMember
from models import Attendance, Grade, Member


def load_member_data() -> list[Member]:
    """メンバーデータの読み込み"""
    member_data_path = Path(__file__).parents[1] / "data" / "member.json"
    with open(member_data_path, "r") as f:
        member_data = [Member(**data) for data in json.load(f)]

    return member_data


def main(args: list[str] | None = None):
    members = load_member_data()
    absents: list[str] = []
    cl = ClassifyMember(members)

    if not args:
        cl.classify()
        attendance_data = cl.get_attendance()
        before_str = ", ".join(attendance_data[Attendance.BEFORE])
        after_str = ", ".join(attendance_data[Attendance.AFTER])
        absent_str = ", ".join(absents)

        meeting_info = {
            "mainText": "明日は研究ミーティングです",
            "firstHalf": f"前半: {before_str}",
            "secondHalf": f"後半: {after_str}",
            "absent": f"欠席: {absent_str}",
        }
        print(json.dumps(meeting_info, ensure_ascii=False, indent=2))
        sys.exit(0)

    elif len(args) > 1:
        if args[1] == "absent":
            if len(args) == 2:
                print("欠席者を指定してください")
                sys.exit(1)

            absents = args[2:]
            cl.classify(absents)
            attendance_data = cl.get_attendance()
            before_str = ", ".join(attendance_data[Attendance.BEFORE])
            after_str = ", ".join(attendance_data[Attendance.AFTER])
            absent_str = ", ".join(absents)

            meeting_info = {
                "mainText": "明日は研究ミーティングです",
                "firstHalf": f"前半: {before_str}",
                "secondHalf": f"後半: {after_str}",
                "absent": f"欠席: {absent_str}",
            }
            print(json.dumps(meeting_info, ensure_ascii=False, indent=2))
            sys.exit(0)

        elif args[1] == "add":
            if len(args) == 2:
                print("追加する人の名前と学年を指定してください")
                sys.exit(1)
            grade_input = args[2]
            if grade_input not in Grade.__members__:
                print(f"{grade_input} は存在しない学年です")
                sys.exit(1)
            name = args[3]
            cl.add_member(Grade[grade_input], name)
            sys.exit(0)

        elif args[1] == "remove":
            if len(args) == 2:
                print("削除する人の名前を指定してください")
                sys.exit(1)
            name = args[2]
            cl.remove_member(name)
            sys.exit(0)
        else:
            print("不正な引数です")
            sys.exit(1)


if __name__ == "__main__":
    args = sys.argv
    main(args)
