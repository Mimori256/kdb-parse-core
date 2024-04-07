from dataclasses import dataclass, asdict, field
import csv
import json
from typing import ClassVar, Dict, List
import logging

# ログの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class Subject:
    class_id: str
    name: str
    module: str
    period: str
    remarks: str
    unit: str
    room: str = field(default=" ")  # デフォルト値を指定

    CSV_HEADER: ClassVar[List[str]] = [
        "科目番号",
        "科目名",
        "授業方法",
        "単位数",
        "標準履修年次",
        "実施学期",
        "曜時限",
        "教室",
        "担当教員",
        "授業概要",
        "備考",
        "科目等履修生申請可否",
        "申請条件",
        "短期留学生申請可否",
        "申請条件",
        "英語(日本語)科目名",
        "科目コード",
        "要件科目名",
        "データ更新日",
    ]

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "Subject":
        return cls(
            class_id=row["科目番号"],
            name=row["科目名"],
            module=row["実施学期"],
            period=row["曜時限"],
            room=row.get("教室", " "),
            remarks=row["備考"],
            unit=row["単位数"].replace(" ", ""),
        )


def convert_csv_to_json(csv_file_path: str, json_file_path: str) -> None:
    data = {}
    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            subject = Subject.from_csv_row(row)
            # 科目番号をキーとして、科目情報をリストとして格納
            # { "科目番号": ["科目名","モジュール","曜時限","教室","備考","単位数"], ・・・}
            data[subject.class_id] = [
                subject.name,
                subject.module,
                subject.period,
                subject.room,
                subject.remarks,
                subject.unit,
            ]

    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
    logging.info(f"CSVデータを'{json_file_path}'へ変換しました。")


if __name__ == "__main__":
    convert_csv_to_json("kdb.csv", "kdb.json")
