import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


class TestGetFileInfo(unittest.TestCase):
    def setUp(self):
        self.get_files_info = get_files_info

    def test_calculator_with_dot(self):
        output = self.get_files_info("calculator", ".")
        print(output)
        testcase = """Result for current directory:
 - main.py: file_size=565 bytes, is_dir=False
 - pkg: file_size=84 bytes, is_dir=True
 - tests.py: file_size=1331 bytes, is_dir=False
 - lorem.txt: file_size=28 bytes, is_dir=False"""
        self.assertEqual(output, testcase)

    def test_calculator_with_pkg(self):
        output = self.get_files_info("calculator", "pkg")
        print(output)
        testcase = """Result for 'pkg' directory:
 - calculator.py: file_size=1721 bytes, is_dir=False
 - render.py: file_size=754 bytes, is_dir=False
 - __pycache__: file_size=70 bytes, is_dir=True
 - morelorem.txt: file_size=26 bytes, is_dir=False"""
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


# For now, we just print output
class TestGetFileContent(unittest.TestCase):
    def setUp(self):
        self.get_file_content = get_file_content

    def test_lorem_ipsum_text_in_calculator_dir(self):
        output = self.get_file_content("calculator", "lorem.txt")
        print(output)

    def test_main_dot_py_in_calculator_dir(self):
        output = self.get_file_content("calculator", "main.py")
        print(output)

    def test_calculator_module_path(self):
        output = self.get_file_content("calculator", "pkg/calculator.py")
        print(output)

    def test_outside_working_dir(self):
        output = self.get_file_content("calculator", "/bin/cat")
        print(output)


# For now, we just print output
class TestWriteFileContent(unittest.TestCase):
    def setUp(self):
        self.write_file = write_file

    def test_write_to_lorem_in_calculator(self):
        output = self.write_file(
            "calculator", "lorem.txt", "wait, this isn't lorem ipsum"
        )
        print(output)

    def test_morelorem_in_calculator(self):
        output = self.write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(output)

    def test_fail_write_outside_workdir(self):
        output = self.write_file(
            "calculator", "/tmp/temp.txt", "this should not be allowed"
        )
        print(output)


if __name__ == "__main__":
    unittest.main()
