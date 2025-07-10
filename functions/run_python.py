import subprocess
import os

TIMEOUT_IN_SECONDS = 30


def run_python_file(working_directory, file_path=None):
    working_directory = os.path.abspath(working_directory)
    joined_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    what_file = "current" if working_directory == joined_file_path else f"'{file_path}'"
    if not joined_file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_file_path) or not os.path.exists(joined_file_path):
        return f'Error: File "{file_path}" not found.'

    if not joined_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    run_args = ["python3", joined_file_path]
    try:
        execute = subprocess.run(
            run_args, timeout=TIMEOUT_IN_SECONDS, capture_output=True, encoding="UTF-8"
        )
        if not execute.stdout:
            return "No output produced."
        stdout = f"STDOUT: {execute.stdout}"
        stderr = f"STDERR: {execute.stderr}"
        output = f"{stdout}\n{stderr}"
        if execute.returncode > 0:
            output = f"{output}\nProcess exited with code {execute.returncode}"
        return output
    except subprocess.SubprocessError as err:
        return f"Error: executing Python file: {err}"
