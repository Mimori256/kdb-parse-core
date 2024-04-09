"""
This module defines the Subject dataclass.

The Subject dataclass represents a subject with its attributes.
It provides a convenient way to create and manipulate subject objects.


Example usage:
    subject = Subject(
        class_id="GC22201",
        name="プログラム言語論",
        method="1",
        credits="2.0",
        standard_course_year="3・4",
        module="春AB",
        period="木1,2",
        teaching_staff="志築 文太郎",
        class_outline="さまざまなプログラミング言語が提供する諸概念を、そのメカニズム、プログラミング手法、適用分野、実現方法などの観点から概説する。",
        remarks="実習設備の都合により、70名程度を受講者数の上限とする。履修希望者が上限を越えた場合には、情報メディア創成学類の学生を優先する。 対面(オンライン併用型)",
        enrollment_application="△",
        enrollment_requirements="実習を伴って実施するため,実習用設備の範囲内に限り受け入れ可(ただしほとんど余裕はない)",
        short_term_students_application="×",
        short_term_students_requirements="",
        english_name="Programming Languages and Methodology",
        subject_code="GC50301",
        requirement_subject_name="プログラム言語論",
        data_update_date="2024-03-18 11:19:41",
        room="7C202"
    )


Attributes:
    class_id (str): The ID of the subject.
    name (str): The name of the subject.
    method (str): The teaching method of the subject.
    credits (str): The number of credits for the subject.
    standard_course_year (str): The standard course year for the subject.
    module (str): The module in which the subject is offered.
    period (str): The schedule of the subject.
    teaching_staff (str): The teaching staff for the subject.
    class_outline (str): The outline of the subject.
    remarks (str): Any additional remarks for the subject.
    enrollment_application (str): The availability of enrollment application for the subject.
    enrollment_requirements (str): The requirements for enrollment in the subject.
    short_term_students_application (str): The availability of enrollment application for short-term
    students.
    short_term_students_requirements (str): The requirements for enrollment of short-term students.
    english_name (str): The English name of the subject.
    subject_code (str): The code of the subject.
    requirement_subject_name (str): The name of the requirement subject.
    data_update_date (str): The date of data update for the subject.
    room (str): The room where the subject is held.

"""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List


@dataclass
class Subject:
    """
    Represents a subject with its attributes.
    """

    class_id: str
    name: str
    method: str
    credits: str
    standard_course_year: str
    module: str
    period: str
    teaching_staff: str
    class_outline: str
    remarks: str
    enrollment_application: str
    enrollment_requirements: str
    short_term_students_application: str
    short_term_students_requirements: str
    english_name: str
    subject_code: str
    requirement_subject_name: str
    data_update_date: str
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
        """
        Creates a Subject instance from a CSV row.

        Args:
            row (Dict[str, str]): A dictionary representing a row of CSV data.

        Returns:
            Subject: A Subject instance created from the CSV row.
        """
        return cls(
            class_id=row["科目番号"],
            name=row["科目名"],
            method=row["授業方法"],
            credits=row["単位数"].strip(),
            standard_course_year=row["標準履修年次"],
            module=row["実施学期"],
            period=row["曜時限"],
            teaching_staff=row["担当教員"],
            class_outline=row["授業概要"],
            enrollment_application=row["科目等履修生申請可否"],
            enrollment_requirements=row["申請条件"],
            short_term_students_application=row["短期留学生申請可否"],
            short_term_students_requirements=row["申請条件"],
            english_name=row["英語(日本語)科目名"],
            subject_code=row["科目コード"],
            requirement_subject_name=row["要件科目名"],
            data_update_date=row["データ更新日"],
            room=row.get("教室", " "),
            remarks=row["備考"],
        )
