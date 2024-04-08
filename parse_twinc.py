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
from dataclasses import dataclass
from typing import List, Literal, TypedDict

WEEKDAY_LIST = ["月", "火", "水", "木", "金", "土", "日"]
SEASONS = ["春", "秋"]
MODULE_LIST = ["春A", "春B", "春C", "秋A", "秋B", "秋C", "夏季休業中", "春季休業中"]
SPRING_MODULE_LIST = ["春A", "春B", "春C"]
FALL_MODULE_LIST = ["秋A", "秋B", "秋C"]
SPECIAL_MODULE_LIST = ["夏季休業中", "春季休業中"]


class Table(TypedDict):
    """Type definition for the table data."""

    period: List[List[bool]]
    focus: bool
    negotiable: bool
    asneeded: bool


class Class:
    def __init__(self, class_id, name, module, period_tmp, room, description):
        self.class_id = class_id
        self.name = name
        self.module = module
        self.period_tmp = period_tmp
        self.room = room
        self.description = description
        self.terms = []
        self.period = []

    def as_json(self):
        return {
            "class_id": self.class_id,
            "name": self.name,
            "module": self.terms,
            "period": self.period,
            "room": self.room,
            "description": self.description,
        }

    def parsed_module(self):
        module = self.terms

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


def create_class_list(input_file: str, name_field_number: int) -> List[Class]:

    with open(input_file, "r", encoding="utf_8") as f:
        class_list = []
        lines = f.readlines()

        # Remove the header
        lines.pop(0)

        for line in lines:
            tmp = line.split('"')
            class_id = tmp[1]
            name = tmp[name_field_number]
            module = tmp[11]
            period_tmp = tmp[13]
            room = tmp[15]
            description = tmp[21]

            if room == "":
                room = " "

            # Remove classes that are not opened in this year
            if not "" in set([class_id, name, module, period_tmp, room, description]):
                class_list.append(
                    Class(class_id, name, module, period_tmp, room, description)
                )

        return class_list


def create_timetable():
    return [[False] * 8 for _ in range(7)]


def parse_timetable(table: Table) -> List[str]:
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


def convert_csv_to_twinc_json(
    name_field_number: int, input_file: str, output_file: str
) -> None:
    subject_map = {}

    class_list = create_class_list(
        input_file=input_file, name_field_number=name_field_number
    )

    for course in class_list:

        term_groups = course.module.split(" ")
        season = ""

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
            course.terms.append(module_group)

        term_str_array = course.period_tmp.split(" ")

        for i, term in enumerate(term_str_array):
            period_str_array = term.split(",")
            day_array = []
            course.period.append(
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
                    start_time = int(time_str_array[0])
                    end_time = int(time_str_array[1])
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
                            course.period[i]["period"][day][time - 1] = True

        course.period = [parse_timetable(x) for x in course.period]

        course.terms = course.parsed_module()

        if course.terms == [[]]:
            course.terms = [["通年"]]

        subject_map[course.class_id] = course.as_json()

    enc = json.dumps(subject_map, ensure_ascii=False, indent=2)
    with open(output_file, "w", encoding="utf_8") as f:
        f.write(enc)
    print("complete")


@dataclass
class ParseTwincLang:
    """
    Dataclass for storing the name field number and output file for a language.
    """

    name_field_number: int
    output_file: str


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_twinc.py <lang>")
        sys.exit(1)
    elif sys.argv[1] not in ["ja", "en"]:
        print("Invalid language. Please specify 'ja' or 'en'.")
        sys.exit(1)

    lang = {
        "ja": ParseTwincLang(3, "kdb_twinc.json"),
        "en": ParseTwincLang(31, "kdb_twinc_en.json"),
    }[sys.argv[1]]

    convert_csv_to_twinc_json(
        name_field_number=lang.name_field_number,
        input_file="kdb.csv",
        output_file=lang.output_file,
    )
