"""
This module provides functions for parsing a CSV file and converting it to a
JSON file.

It defines a dataclass called Subject, which represents a subject with its
attributes.
The module also includes a function called convert_csv_to_json, which takes a
CSV file path and a JSON file path as input and converts the CSV file to a
JSON file.

Example usage:
    convert_csv_to_json("kdb.csv", "kdb.json")
"""

import csv
import json
import logging

from subject_dataclass import Subject

# ログの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_csv_to_json(csv_file_path: str, json_file_path: str) -> None:
    """
    Converts a CSV file to a JSON file.

    Args:
        csv_file_path (str): The path to the CSV file.
        json_file_path (str): The path to the JSON file.

    Returns:
        None
    """
    data = {}
    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=Subject.CSV_HEADER)
        next(csv_reader) # Skip the header row
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
                subject.credits
            ]

    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        logging.info("CSVデータを'%s'へ変換しました。", json_file_path)


if __name__ == "__main__":
    convert_csv_to_json("kdb.csv", "kdb.json")
