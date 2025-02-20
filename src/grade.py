import math
import random

from models import Attendance, Member


class GradeClassifier:
    def __init__(self, members: list[Member], attendance_data: dict[Attendance, list[str]], weight: int):
        self.attendance_data = attendance_data
        self.next_members: list[Member] = []
        self.members = members
        self.border = math.ceil((len(members) + weight) / 2)
        self.weight = weight
        self.before_count = weight
        self.after_count = 0

    def classify(self, absents: list[str] | None = None):
        """前後半に分ける"""
        for member in self.members:
            # 欠席者の処理
            if absents and member.name in absents:
                self._update_attendance(member, Attendance.ABSENT)
                self.border = math.ceil((len(self.members) - 1 + self.weight) / 2)
                continue
            self._check_same_half(member)

        while self.members:
            self._select_half(self.members[0])

    def get_next_member(self) -> list[Member]:
        """処理を行った後のメンバーの状態を返す"""
        return self.next_members

    def get_count(self) -> tuple[int, int]:
        """前半と後半の数をタプル形式で返す"""
        return self.before_count, self.after_count

    def _check_same_half(self, member: Member) -> None:
        """2回連続前半か後半かになっているか確認"""
        if member.last == member.previous == Attendance.BEFORE:
            self._update_attendance(member, Attendance.AFTER)
        elif member.last == member.previous == Attendance.AFTER:
            self._update_attendance(member, Attendance.BEFORE)

    def _select_half(self, member: Member):
        """前後半を比較し，定員以上ならばもう一方に入れ，定員未満ならランダムで決定"""
        choice = [Attendance.BEFORE, Attendance.AFTER]

        if self.after_count == self.border:
            self._update_attendance(member, Attendance.BEFORE)
        elif self.before_count == self.border:
            self._update_attendance(member, Attendance.AFTER)
        else:
            rand = random.randint(0, 1)
            self._update_attendance(member, choice[rand])

    def _update_attendance(self, member: Member, next: Attendance):
        """出席情報の更新"""
        member.previous = member.last
        member.last = next
        self.next_members.append(member)
        self.attendance_data[next].append(member.name)

        # 　出席者の数の更新
        if next == Attendance.BEFORE:
            self.before_count += 1
        elif next == Attendance.AFTER:
            self.after_count += 1

        self.members.remove(member)
