"""
Converts CSV data to grad check JSON format.
"""

import json
import csv
from dataclasses import dataclass, asdict
from typing import Dict, List
import logging
from subject_dataclass import Subject

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class GradCheckSubject:
    """
    Represents a subject with its attributes for grad check.
    """
    id: str
    name: str
    credits: str
    registerYear: str
    modules: str
    period: str


def convert_csv_to_grad_check(input_path: str, output_path: str) -> None:
    """
    Main function that converts CSV data to grad check JSON format.
    """
    data: Dict[str, List[Dict[str, str]]] = {"courses": []}

    with open(input_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=Subject.CSV_HEADER)
        next(csv_reader)  # Skip the header row
        subjects = [Subject.from_csv_row(row) for row in csv_reader]

        data["courses"] = [
            asdict(GradCheckSubject(
                id=subject.class_id,
                name=subject.name,
                credits=subject.credits,
                registerYear=subject.standard_course_year,
                modules=subject.module,
                period=subject.period,
            ))
            for subject in subjects
            if subject.class_id and subject.class_id[0] == "G"
        ]

    with open(output_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        logging.info("CSVデータを'%s'へ変換しました。", output_path)


if __name__ == "__main__":
    INPUT_PATH = "kdb.csv"
    OUTPUT_PATH = "kdb_gradcheck.json"
    convert_csv_to_grad_check(INPUT_PATH, OUTPUT_PATH)
