import os
import unittest
import json
from parse import convert_csv_to_json

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
        input_csv_path = 'testdata/sample_kdb.csv'  # サンプルCSVファイル
        output_json_path = 'testdata/test_kdb.json'  # 出力JSONファイルのパス
        expected_output_path = 'testdata/sample_kdb.json'  # 期待される出力JSONファイルのパス

        # 変換を実行
        convert_csv_to_json(input_csv_path, output_json_path)

        # 変換結果の検証
        with open(output_json_path, mode='r', encoding='utf-8') as f:
            actual_data = json.load(f)
        
        # 期待される結果との比較
        with open(expected_output_path, mode='r', encoding='utf-8') as f:
            expected_data = json.load(f)
        
        # データが辞書であることを確認
        self.assertIsInstance(actual_data, dict)
        self.assertIsInstance(expected_data, dict)

        # 出力が期待される結果と一致することを確認
        self.assertEqual(actual_data, expected_data)

        # さらに詳細な検証を行う
        for class_id, info in actual_data.items():
            self.assertIsInstance(class_id, str)
            self.assertIsInstance(info, list)
            self.assertEqual(len(info), 6)  # 科目情報の要素数が正しいか確認

        # testdata/test_output.jsonを削除
        os.remove(output_json_path)

if __name__ == '__main__':
    unittest.main()
