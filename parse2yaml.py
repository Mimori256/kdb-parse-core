"""
This script converts CSV data to YAML format.

It defines a function called main, which converts the CSV data to YAML format

Example usage:
    main()
"""

import logging
import csv
from dataclasses import asdict
from typing import Dict, List
import yaml
from subject_dataclass import Subject

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def convert_csv_to_yaml(input_path: str, output_path: str) -> None:
    """
    Main function that converts CSV data to YAML format.
    """
    subjects: List[Dict[str, str]] = []
    with open(input_path, mode="r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, fieldnames=Subject.CSV_HEADER)
        next(csv_reader)  # Skip the header row
        subjects = [asdict(Subject.from_csv_row(row)) for row in csv_reader]

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(subjects, f, allow_unicode=True)

    logging.info("Conversion completed.")


if __name__ == "__main__":
    convert_csv_to_yaml("kdb.csv", "kdb.yaml")
