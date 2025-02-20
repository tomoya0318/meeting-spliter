import json
import random
from collections import OrderedDict, defaultdict
from pathlib import Path

from grade import GradeClassifier
from models import Attendance, Grade, Member


class ClassifyMember:
    def __init__(self, members: list[Member]):
        self.members = members
        self.attendance_data: dict[Attendance, list[str]] = defaultdict(list)
        self.grade_weight_map = self._random_grade_weight()

    def classify(self, absents: list[str] | None = None):
        """メンバーを前後半に分ける"""
        # 学年ごとに分ける
        grouped_by_grade = defaultdict(list)
        for member in self.members:
            grouped_by_grade[member.grade].append(member)
        sorted_grouped_by_grade = OrderedDict(sorted(grouped_by_grade.items(), key=lambda x: self._grade_weight(x[0])))

        # 以下の行はランダムに学年を並び替えるための処理だが未実装
        # sorted_grouped_by_grade = OrderedDict(
        #     sorted(grouped_by_grade.items(), key=lambda x: self.grade_weight_map[x[0]])
        # )

        # 学年ごとに前後半を判定
        next_members: list[Member] = []
        weight = 0
        for members in sorted_grouped_by_grade.values():
            GC = GradeClassifier(members, self.attendance_data, weight)
            GC.classify(absents)
            next_members.extend(GC.get_next_member())
            before, after = GC.get_count()
            weight = before - after

        self.members = next_members
        self._dump_to_json()

    def get_attendance(self) -> dict[Attendance, list[str]]:
        return self.attendance_data

    def add_member(self, grade: Grade, name: str):
        """メンバー追加（学年と登録名を指定）"""
        member = Member(grade=grade, name=name, last=Attendance.ABSENT, previous=Attendance.ABSENT)
        self.members.append(member)
        self._dump_to_json()

    def remove_member(self, name: str):
        """メンバーを削除（登録名で指定）"""
        self.members = [member for member in self.members if member.name != name]
        self._dump_to_json()

    def _dump_to_json(self):
        members_dict = [member.model_dump() for member in self.members]
        member_data_path = Path(__file__).parents[1] / "data" / "member.json"
        with open(member_data_path, "w", encoding="utf-8") as f:
            json.dump(members_dict, f, ensure_ascii=False, indent=4)

    def _grade_weight(self, grade: Grade) -> int:
        """学年が小さい順で並べるように重みをつける"""
        grade_order = {Grade.B2: 0, Grade.B3: 1, Grade.B4: 2, Grade.M1: 3, Grade.M2: 4}
        return grade_order[grade]

    def _random_grade_weight(self):
        """学年順がランダムになるように重み付け"""
        weight_list = list(range(len(Grade)))
        random.shuffle(weight_list)

        grade_order = {grade: weight_list.pop() for grade in Grade}
        return grade_order
        return grade_order
