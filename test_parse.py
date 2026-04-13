"""
This module contains unit tests for CSV to JSON conversion.

The module includes test cases for converting CSV files to JSON format using different conversion methods.
It verifies the correctness of the conversion process and performs additional validation on the converted data.
"""

import os
import unittest
import json
import csv
import io
import yaml
from download import normalize_csv_text
from parse import convert_csv_to_json
from parse_structural import convert_csv_to_structural_json
from parse2yaml import convert_csv_to_yaml
from parse_twinc import convert_csv_to_twinc_json
from parse_twinc import subject_to_class
from parse_gradcheck import convert_csv_to_gradcheck
from subject_dataclass import Subject


class TestCSVtoJSONConversion(unittest.TestCase):
    """
    Unit tests for CSV to JSON conversion.

    This test case class contains unit tests for the conversion of CSV to JSON.
    It verifies the correctness of the conversion process and performs additional
    validation on the converted data.

    """

    def test_conversion(self):
        """
        Test the conversion of CSV to JSON.

        This method performs the following steps:
        1. Defines the paths for input CSV file, output JSON file, and expected output JSON file.
        2. Executes the conversion by calling the `convert_csv_to_json` function.
        3. Verifies the conversion result by comparing the actual output JSON with the expected output JSON.
        4. Performs additional detailed validation on the converted data.

        Raises:
            AssertionError: If the conversion result does not match the expected output.

        """
        input_csv_path = "sample_data/kdb.csv"  # サンプルCSVファイル
        output_json_path = "test_data/kdb.json"  # 出力JSONファイルのパス
        expected_output_path = (
            "sample_data/kdb.json"  # 期待される出力JSONファイルのパス
        )

        # 変換を実行
        convert_csv_to_json(input_csv_path, output_json_path)

        # 変換結果の検証
        with open(output_json_path, mode="r", encoding="utf-8") as f:
            actual_data = json.load(f)

        # 期待される結果との比較
        with open(expected_output_path, mode="r", encoding="utf-8") as f:
            expected_data = json.load(f)

        # データが辞書であることを確認
        self.assertIsInstance(actual_data, dict)
        self.assertIsInstance(expected_data, dict)

        # 出力が期待される結果と一致することを確認
        self.assertDictEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for class_id, info in actual_data.items():
            self.assertIsInstance(class_id, str)
            self.assertIsInstance(info, list)
            self.assertEqual(len(info), 6)  # 科目情報の要素数が正しいか確認

        # test_data/output.jsonを削除
        os.remove(output_json_path)

    def test_parse_structural(self):
        """
        Test the conversion of CSV to structured JSON.

        This method performs the following steps:
        1. Defines the paths for input CSV file, output JSON file, and expected output JSON file.
        2. Executes the conversion by calling the `convert_csv_to_structural_json` function.
        3. Verifies the conversion result by comparing the actual output JSON with the expected output JSON.
        4. Performs additional detailed validation on the converted data.

        Raises:
            AssertionError: If the conversion result does not match the expected output.

        """
        input_csv_path = "sample_data/kdb.csv"
        output_json_path = "test_data/kdb_structural_output.json"
        expected_output_path = "sample_data/kdb_structural.json"

        # 変換を実行
        convert_csv_to_structural_json(input_csv_path, output_json_path)

        # 変換結果の検証
        with open(output_json_path, mode="r", encoding="utf-8") as f:
            actual_data = json.load(f)

        # 期待される結果との比較
        with open(expected_output_path, mode="r", encoding="utf-8") as f:
            expected_data = json.load(f)

        # データが辞書であることを確認
        self.assertIsInstance(actual_data, dict)
        self.assertIsInstance(expected_data, dict)

        # 出力が期待される結果と一致することを確認
        self.assertDictEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for course in actual_data["courses"]:
            self.assertIsInstance(course, dict)
            self.assertEqual(len(course), 19)

        # test_data/kdb_structural_output.jsonを削除
        os.remove(output_json_path)

    def test_parse2yaml(self):
        """
        Test the conversion of CSV to YAML.

        This method performs the following steps:
        1. Defines the paths for input CSV file, output YAML file, and expected output YAML file.
        2. Executes the conversion by calling the `convert_csv_to_yaml` function.
        3. Verifies the conversion result by comparing the actual output YAML with the expected output YAML.
        4. Performs additional detailed validation on the converted data.

        Raises:
            AssertionError: If the conversion result does not match the expected output.

        """
        input_csv_path = "sample_data/kdb.csv"
        output_path = "test_data/kdb.yaml"
        expected_output_path = "sample_data/kdb.yaml"

        # 変換を実行
        convert_csv_to_yaml(input_csv_path, output_path)

        # 変換結果の検証
        with open(output_path, mode="r", encoding="utf-8") as f:
            actual_data = yaml.safe_load(f)

        # 期待される結果との比較
        with open(expected_output_path, mode="r", encoding="utf-8") as f:
            expected_data = yaml.safe_load(f)

        # データがリストであることを確認
        self.assertIsInstance(actual_data, list)
        self.assertIsInstance(expected_data, list)

        # 出力が期待される結果と一致することを確認
        self.assertListEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for subject in actual_data:
            self.assertIsInstance(subject, dict)
            self.assertEqual(len(subject), 19)

        # test_data/kdb_structural_output.jsonを削除
        os.remove(output_path)

    def test_kdb_twinc_ja_json(self):
        """
        Test the conversion of CSV to JSON for the Japanese language.

        This method performs the following steps:
        1. Defines the paths for input CSV file, output JSON file, and expected output JSON file.
        2. Executes the conversion by calling the `convert_csv_to_json` function.
        3. Verifies the conversion result by comparing the actual output JSON with the expected output JSON.
        4. Performs additional detailed validation on the converted data.

        Raises:
            AssertionError: If the conversion result does not match the expected output.

        """
        input_csv_path = "sample_data/kdb.csv"
        output_json_path = "test_data/kdb_twinc.json"
        expected_output_path = "sample_data/kdb_twinc.json"

        # 変換を実行
        convert_csv_to_twinc_json(
            lang="ja", input_file=input_csv_path, output_file=output_json_path
        )

        # 変換結果の検証
        with open(output_json_path, mode="r", encoding="utf-8") as f:
            actual_data = json.load(f)

        # 期待される結果との比較
        with open(expected_output_path, mode="r", encoding="utf-8") as f:
            expected_data = json.load(f)

        # データが辞書であることを確認
        self.assertIsInstance(actual_data, dict)
        self.assertIsInstance(expected_data, dict)

        # 出力が期待される結果と一致することを確認
        self.assertDictEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for class_id, info in actual_data.items():
            self.assertIsInstance(class_id, str)
            self.assertIsInstance(info, dict)
            self.assertEqual(len(info), 6)

        # test_data/kdb_twinc_ja.jsonを削除
        os.remove(output_json_path)

    def test_kdb_twinc_en_json(self):
        """
        Test the conversion of CSV to JSON for the English language.

        This method performs the following steps:
        1. Defines the paths for input CSV file, output JSON file, and expected output JSON file.
        2. Executes the conversion by calling the `convert_csv_to_json` function.
        3. Verifies the conversion result by comparing the actual output JSON with the expected output JSON.
        4. Performs additional detailed validation on the converted data.

        Raises:
            AssertionError: If the conversion result does not match the expected output.

        """
        input_csv_path = "sample_data/kdb.csv"
        output_json_path = "test_data/kdb_twinc_en.json"
        expected_output_path = "sample_data/kdb_twinc_en.json"

        # 変換を実行
        convert_csv_to_twinc_json(
            lang="en",
            input_file=input_csv_path,
            output_file=output_json_path,
        )

        # 変換結果の検証
        with open(output_json_path, mode="r", encoding="utf-8") as f:
            actual_data = json.load(f)

        # 期待される結果との比較
        with open(expected_output_path, mode="r", encoding="utf-8") as f:
            expected_data = json.load(f)

        # データが辞書であることを確認
        self.assertIsInstance(actual_data, dict)
        self.assertIsInstance(expected_data, dict)

        # 出力が期待される結果と一致することを確認
        self.assertDictEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for class_id, info in actual_data.items():
            self.assertIsInstance(class_id, str)
            self.assertIsInstance(info, dict)
            self.assertEqual(len(info), 6)

        # test_data/kdb_twinc_en.jsonを削除
        os.remove(output_json_path)

 
    def test_kdb_gradcheck_json(self):
        """
        Test the conversion of CSV to JSON for grad check.

        This method performs the following steps:
        1. Defines the paths for input CSV file, output JSON file, and expected output JSON file.
        2. Executes the conversion by calling the `convert_csv_to_json` function.
        3. Verifies the conversion result by comparing the actual output JSON with the expected output JSON.
        4. Performs additional detailed validation on the converted data.

        Raises:
            AssertionError: If the conversion result does not match the expected output.

        """
        input_csv_path = "sample_data/kdb.csv"
        output_json_path = "test_data/kdb_gradcheck.json"
        expected_output_path = "sample_data/kdb_gradcheck.json"

        # 変換を実行
        convert_csv_to_gradcheck(input_csv_path, output_json_path)

        # 変換結果の検証
        with open(output_json_path, mode="r", encoding="utf-8") as f:
            actual_data = json.load(f)

        # 期待される結果との比較
        with open(expected_output_path, mode="r", encoding="utf-8") as f:
            expected_data = json.load(f)

        # データが辞書であることを確認
        self.assertIsInstance(actual_data, dict)
        self.assertIsInstance(expected_data, dict)

        # 出力が期待される結果と一致することを確認
        self.assertDictEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for _, course in enumerate(actual_data["courses"]):
            self.assertIsInstance(course, dict)
            self.assertEqual(len(course), 6)

        # test_data/kdb_gradcheck.jsonを削除
        os.remove(output_json_path)

    def test_normalize_current_kdb_csv(self):
        with open("sample_data/kdb_current.csv", mode="r", encoding="utf-8") as f:
            normalized_csv = normalize_csv_text(f.read())

        rows = list(csv.reader(io.StringIO(normalized_csv)))

        self.assertEqual(rows[0], Subject.CSV_HEADER)
        self.assertEqual(len(rows[1]), len(Subject.CSV_HEADER))
        self.assertEqual(rows[1][7], "")
        self.assertEqual(rows[1][8], "教員A")
        self.assertEqual(rows[2][5], "秋ABC")
        self.assertEqual(rows[2][7], "")

    def test_subject_to_class_with_newline_separated_terms(self):
        subject = Subject(
            class_id="01TEST3",
            name="改行区切り科目",
            method="1",
            credits="1.0",
            standard_course_year="1",
            module="春A\n春B",
            period="土4,5\n土6,7",
            teaching_staff="教員C",
            class_outline="概要C",
            remarks="備考C",
            enrollment_application="×",
            enrollment_requirements="条件C",
            short_term_students_application="",
            short_term_students_requirements="",
            english_name="Newline Terms Course",
            subject_code="0TEST03",
            requirement_subject_name="改行区切り科目",
            data_update_date="2026-04-13 00:00:00",
            room="",
        )

        parsed = subject_to_class("ja", subject)

        self.assertEqual(parsed.module, [["春A"], ["春B"]])
        self.assertEqual(parsed.period, [["土4", "土5"], ["土6", "土7"]])

    def test_subject_to_class_escapes_multiline_remarks_for_ics(self):
        subject = Subject(
            class_id="01TEST4",
            name="複数行備考科目",
            method="1",
            credits="1.0",
            standard_course_year="1",
            module="春A",
            period="月1",
            teaching_staff="教員D",
            class_outline="概要D",
            remarks="1行目\r\n2行目\n3行目",
            enrollment_application="×",
            enrollment_requirements="条件D",
            short_term_students_application="",
            short_term_students_requirements="",
            english_name="Multiline Remarks Course",
            subject_code="0TEST04",
            requirement_subject_name="複数行備考科目",
            data_update_date="2026-04-14 00:00:00",
            room="",
        )

        parsed = subject_to_class("ja", subject)

        self.assertEqual(parsed.description, "1行目\\n2行目\\n3行目")


if __name__ == "__main__":
    unittest.main()
