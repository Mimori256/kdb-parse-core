"""
This script converts CSV data to YAML format.

It defines a function called main, which converts the CSV data to YAML format

Example usage:
    main()
"""

import logging
import yaml
from parse_structural import csv_to_dict

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main(output_path: str = "output.yaml") -> None:
    """
    Main function that converts CSV data to YAML format.
    """
    courses = csv_to_dict()
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(courses, f, allow_unicode=True)

    logging.info("Conversion completed.")


if __name__ == "__main__":
    main("kdb.yaml")
