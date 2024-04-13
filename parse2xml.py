"""
This script converts a CSV file to XML format based on the specified language.

It defines a function called main, which takes the path to the input CSV file,
the path to the output XML file, and the language used in the CSV file as input
and converts the CSV file to XML format.

Example usage:
    main("kdb.csv", "kdb.xml", "ja")
"""

import csv
import json
from typing import Dict, List
import xml.etree.ElementTree as ET
from enum import Enum


def get_translations(lang: str) -> Dict[str, str]:
    """
    Retrieves translations for a specific language.

    Args:
        lang (str): The language code for the desired translations.

    Returns:
        dict[str, str]: A dictionary containing the translations for the
        specified language.
    """
    with open("translations.json", "r", encoding="utf_8") as f:
        trans: Dict[str, Dict[str, str]] = json.load(f)
        return trans[lang]


def str2tag_name(string: str) -> str:
    """
    Converts a string to a valid XML tag name.

    Args:
        string (str): The input string to be converted.

    Returns:
        str: The converted string with spaces replaced by underscores and
        parentheses removed.

    """
    return string.lower().replace(" ", "_").replace("(", "").replace(")", "")


def course_enum(lang: str) -> Enum:
    """
    Create an enumeration for courses based on the specified language.

    Args:
        lang (str): The language for which the enumeration is created.

    Returns:
        Enum: The enumeration object representing the courses.

    """
    with open("csvHeader.json", "r", encoding="utf_8") as f:
        cols: Dict[str, List[str]] = json.load(f)
        return Enum("Course", cols[lang], start=0)


def insert_attr_element(parent: ET.Element, name: str, value: str) -> ET.Element:
    """
    Inserts a new attribute element into the parent element with the given
    name and value.

    Args:
        parent (ET.Element): The parent element to insert the attribute
        element into.
        name (str): The name of the attribute element.
        value (str): The value of the attribute element.

    Returns:
        ET.Element: The newly created attribute element.
    """
    child = ET.SubElement(parent, str2tag_name(name))
    child.text = value
    return child


def csv2xml(reader, course_enum, lang: str) -> ET.Element:
    """
    Convert CSV data to XML format.

    Args:
        reader: The CSV reader object.
        course_enum: The Course class object.
        lang (str): The language for translations.

    Returns:
        ET.Element: The root element of the XML tree.
    """
    # remove the header
    next(reader)
    root = ET.Element(get_translations(lang)["courses"])
    for course in reader:
        course_element = ET.SubElement(root, get_translations(lang)["course"])
        for attr in map(lambda x: x.name, course_enum):
            insert_attr_element(
                parent=course_element, name=attr, value=course[course_enum[attr].value]
            )

    return root


def main(input_file: str, output_file: str, lang: str):
    """
    Converts a CSV file to XML format based on the specified language.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output XML file.
        lang (str): The language used in the CSV file.

    Returns:
        None
    """
    course = course_enum(lang)

    with open(input_file, "r", encoding="utf_8") as f:
        reader = csv.reader(f)
        root = csv2xml(reader, course, lang)

    with open(output_file, "w", encoding="utf_8") as f:
        f.write(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    main("kdb.csv", "kdb.xml", "ja")
