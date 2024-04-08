"""
This module provides functions for converting a CSV file to a structured JSON file.
"""

import json
import csv
import logging
from dataclasses import asdict
from typing import Dict, List
from subject_dataclass import Subject

def convert_csv_to_structural_json(csv_file_path: str, json_file_path: str) -> None:
    """
    Converts a CSV file to a structured JSON file.

    Args:
        csv_file_path (str): The path to the CSV file.
        json_file_path (str): The path to the JSON file.
    
    Returns:
        None
    """

    data: Dict[str, List[Dict[str, str]]] = {"courses": []}

    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=Subject.CSV_HEADER)
        next(csv_reader) # Skip the header row
        for row in csv_reader:
            subject = Subject.from_csv_row(row)
            data["courses"].append(asdict(subject))

    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        logging.info("CSVデータを'%s'へ変換しました。", json_file_path)


if __name__ == "__main__":
    convert_csv_to_structural_json("kdb.csv", "kdb_structural.json")
