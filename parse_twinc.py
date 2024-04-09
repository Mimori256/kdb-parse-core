"""
This script parses a CSV file containing class information
and generates a JSON file with the parsed data.

The CSV file should have the following columns:
- Class ID
- Name
- Module
- Period
- Room
- Description

The script reads the CSV file, filters out classes that are not opened in the current year, and parses the module and period information for each class. It then generates a JSON file with the parsed data.

Usage: python parse_twinc.py <lang>
- <lang>: Language code, either 'ja' for Japanese or 'en' for English.

The output JSON file will be named 'kdb_twinc.json' for Japanese
and 'kdb_twinc_en.json' for English.
"""

import json
import re
import sys
import csv
from dataclasses import dataclass, field, asdict
from typing import List, Literal, TypedDict, Dict
import logging
from subject_dataclass import Subject

WEEKDAY_LIST = ("月", "火", "水", "木", "金", "土", "日")
SEASONS = ("春", "秋")
MODULE_LIST = ("春A", "春B", "春C", "秋A", "秋B", "秋C", "夏季休業中", "春季休業中")
SPRING_MODULE_LIST = ("春A", "春B", "春C")
FALL_MODULE_LIST = ("秋A", "秋B", "秋C")
SPECIAL_MODULE_LIST = ("夏季休業中", "春季休業中")


class PeriodTable(TypedDict):
    """Type definition for the table data."""

    period: List[List[bool]]
    focus: bool
    negotiable: bool
    asneeded: bool


Lang = Literal["ja", "en"]
Terms = List[List[str]]


@dataclass
class Class:
    class_id: str
    name: str
    description: str
    module: List[List[str]] = field(default_factory=list)
    period: List[List[str]] = field(default_factory=list)
    room: str = field(default=" ")  # デフォルト値を指定


def parsed_module(terms: Terms) -> List[List[str]]:
    """
    This function parses the module list and returns a list of module strings.

    Args:
        terms (Terms): The module list.

    Returns:
        List[List[str]]: A list of module strings.
    """
    module = terms

    for i, v in enumerate(module):
        res = []
        special_module_list = []
        spring_table, fall_table = [False, False, False], [False, False, False]

        for _, w in enumerate(v):
            if w in SPRING_MODULE_LIST:
                spring_table[SPRING_MODULE_LIST.index(w)] = True
            elif w in FALL_MODULE_LIST:
                fall_table[FALL_MODULE_LIST.index(w)] = True
            # 夏季休業中 or 春季休業中
            else:
                special_module_list.append(w)

        if any(spring_table):
            res.append(check_table(spring_table, "春"))
        if any(fall_table):
            res.append(check_table(fall_table, "秋"))

        for element in special_module_list:
            res.append(element)

        module[i] = res

    return module


def check_table(table: List[bool], season: Literal["春", "秋"]) -> str:
    """
    This function checks the module table and returns the corresponding module string.

    Args:
        table (List[bool]): The module table.
        season (Literal["春", "秋"]): The season.

    Example:
        check_table([True, False, True], "春") -> "春AC"
        check_table([False, False, True], "秋") -> "秋C"
        check_table([False, False, False], "春") -> ValueError
    """

    if not any(table):
        raise ValueError("No module found in the table.")

    return season + "".join([x for x, y in zip(["A", "B", "C"], table) if y])


def subjects_from_csv(input_file: str) -> List[Subject]:
    """
    This function reads the CSV file and creates a list of Subject dataclass instances.

    Args:
        input_file (str): The input CSV file.
        lang (Lang): The language code.

    Returns:
        List[Subject]: A list of Subject dataclass instances.
    """
    with open(input_file, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=Subject.CSV_HEADER)
        next(csv_reader)  # Skip the header row

        return [Subject.from_csv_row(row) for row in csv_reader]


def create_timetable():
    """This function creates an empty timetable."""
    return [[False] * 8 for _ in range(7)]


def parse_timetable(table: PeriodTable) -> List[str]:
    blank_table = create_timetable()

    if table["period"] == blank_table:
        if table["focus"]:
            return ["集中"]
        elif table["negotiable"]:
            return ["応談"]
        else:
            return ["随時"]

    return [
        WEEKDAY_LIST[i] + str(j + 1)
        for i in range(7)
        for j in range(8)
        if table["period"][i][j]
    ]


def convert_csv_to_twinc_json(lang: Lang, input_file: str, output_file: str) -> None:
    """This function converts the CSV file to a JSON file in the TwinC format."""
    subjects = subjects_from_csv(input_file=input_file)
    classes = {
        subject.class_id: subject_to_class_dict(lang, subject) for subject in subjects
    }

    with open(output_file, "w", encoding="utf_8") as f:
        enc = json.dumps(classes, ensure_ascii=False, indent=2)
        f.write(enc)
        logging.info("Successfully converted CSV to JSON.")


def subject_to_class_dict(lang: Lang, subject: Subject) -> Dict[str, str]:
    """
    This function converts a Subject instance to a dictionary.

    Args:
        lang (Lang): The language code.
        subject (Subject): The Subject instance.

    Returns:
        Dict[str, str]: A dictionary containing the class information.
    """
    terms = raw_module_to_terms(subject.module)
    boolean_periods: List[PeriodTable] = []

    term_str_array = subject.period.split(" ")

    for i, term in enumerate(term_str_array):
        period_str_array = term.split(",")
        day_array = []
        boolean_periods.append(
            {
                "focus": term.find("集中") > -1,
                "negotiable": term.find("応談") > -1,
                "asneeded": term.find("随時") > -1,
                "period": create_timetable(),
            }
        )

        for p in period_str_array:
            days = [
                WEEKDAY_LIST.index(x)
                for x in re.sub("[0-9\\-]", "", p).split("・")
                if x in WEEKDAY_LIST
            ]

            if len(days) > 0:
                day_array = days

            time_array: List[int] = []
            time_str = re.sub("[^0-9\\-]", "", p)

            if time_str.find("-") > -1:
                time_str_array = time_str.split("-")
                start_time, end_time = map(int, time_str_array)
                for j in range(start_time, end_time + 1, 1):
                    time_array.append(j)

            else:
                if time_str != "":
                    time_array.append(int(time_str))
                else:
                    time_array.append(0)

            if len(time_str) > 0:
                for day in day_array:
                    for time in time_array:
                        boolean_periods[i]["period"][day][time - 1] = True

    period_ = [parse_timetable(x) for x in boolean_periods]
    parsed_terms = parsed_module(terms) if terms != [[]] else [["通年"]]

    cls = Class(
        class_id=subject.class_id,
        name=subject.name if lang == "ja" else subject.english_name,
        module=parsed_terms,  # Module is stored in the 'Module' field
        period=period_,
        room=(
            subject.room if subject.room != "" else " "
        ),  # Room is stored in the 'Room' field
        description=subject.remarks,  # Description is stored in the 'Remarks' field
    )

    return asdict(cls)


def raw_module_to_terms(raw_module: str) -> Terms:
    """
    This function converts the raw module string to a list of terms.

    Args:
        raw_module (str): The raw module string.

    Returns:
        Terms: A list of terms.
    """
    term_groups = raw_module.split(" ")
    season = ""
    terms = []

    for group_str in term_groups:
        group = []
        char_array = list(group_str)

        for char in char_array:
            if char in SEASONS:
                season = char

            if season != "":
                if char in ["A", "B", "C"]:
                    if season == "春":
                        no = 0
                    else:
                        no = 3

                    if char == "A":
                        no += 0
                    elif char == "B":
                        no += 1
                    else:
                        no += 2
                    group.append(no)

                if char == "休":
                    group.append(SEASONS.index(season) + 6)

        module_group = [MODULE_LIST[x] for x in group]
        terms.append(module_group)

    return terms


@dataclass
class ParseTwincLang:
    """
    Dataclass for storing output file for a language.
    """

    lang: Lang
    output_file: str


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_twinc.py <lang>")
        sys.exit(1)
    elif (arg_lang := sys.argv[1]) not in ["ja", "en"]:
        print("Invalid language. Please specify 'ja' or 'en'.")
        sys.exit(1)

    langs = {
        "ja": ParseTwincLang("ja", "kdb_twinc.json"),
        "en": ParseTwincLang("en", "kdb_twinc_en.json"),
    }[arg_lang]

    convert_csv_to_twinc_json(
        lang=langs.lang,
        input_file="sample_data/kdb.csv",
        output_file=langs.output_file,
    )
