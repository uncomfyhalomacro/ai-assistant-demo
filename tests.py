import unittest
from functions.get_files_info import get_files_info

class TestGetFileInfo(unittest.TestCase):
    def setUp(self):
        self.get_files_info = get_files_info

    def test_calculator_with_dot(self):
        output = self.get_files_info("calculator", ".")
        print(output)
        testcase = """Result for current directory:
 - main.py: file_size=565 bytes, is_dir=False
 - pkg: file_size=63 bytes, is_dir=True
 - tests.py: file_size=1331 bytes, is_dir=False"""
        self.assertEqual(output, testcase)

    def test_calculator_with_pkg(self):
        output = self.get_files_info("calculator", "pkg")
        print(output)
        testcase="""Result for 'pkg' directory:
 - calculator.py: file_size=1721 bytes, is_dir=False
 - render.py: file_size=754 bytes, is_dir=False
 - __pycache__: file_size=70 bytes, is_dir=True"""
        self.assertEqual(output, testcase)

    def test_calculator_with_slash_bin(self):
        output = self.get_files_info("calculator", "/bin")
        print(output)
        testcase = """Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory"""
        self.assertEqual(output, testcase)

    def test_calculator_with_double_dot(self):
        output1 = self.get_files_info("calculator", "..")
        output2 = self.get_files_info("calculator", "../")
        print(output1, output2)
        testcase1 = """Result for '..' directory:
    Error: Cannot list ".." as it is outside the permitted working directory"""
        testcase2 = """Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory"""
        self.assertEqual(output1, testcase1)
        self.assertEqual(output2, testcase2)

if __name__ == "__main__":
    unittest.main()
