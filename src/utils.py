import json
import os
from pathlib import Path

from models import Member


def ensure_dir_exists(file_path: Path):
    """指定されたファイルパスのディレクトリが存在するか確認し、存在しない場合は作成"""
    dir = file_path.parent
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
        print(f"Directory created: {dir}")


def load_member_data() -> list[Member]:
    """メンバーデータの読み込み"""
    member_data_path = Path(__file__).parents[1] / "data" / "member.json"
    ensure_dir_exists(member_data_path)
    try:
        with open(member_data_path, "r") as f:
            member_data = [Member(**data) for data in json.load(f)]
    except FileNotFoundError:
        member_data = []
    return member_data
