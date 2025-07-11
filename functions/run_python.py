import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run and execute python files that are constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, it will return an error message.",
            ),
        },
    ),
)

TIMEOUT_IN_SECONDS = 30


def run_python_file(working_directory, file_path=None):
    if not file_path:
        return "Error: Path to a Python file was not specified."
    working_directory = os.path.abspath(working_directory)
    joined_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not joined_file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_file_path) or not os.path.exists(joined_file_path):
        return f'Error: File "{file_path}" not found.'

    if not joined_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    run_args = ["python3", joined_file_path]
    try:
        execute = subprocess.run(
            run_args, timeout=TIMEOUT_IN_SECONDS, capture_output=True, text=True
        )
        if (execute.stdout is not None and execute.stdout != "") or (
            execute.stderr is not None and execute.stderr != ""
        ):
            stdout = f"STDOUT: {execute.stdout}"
            stderr = f"STDERR: {execute.stderr}"
            output = f"{stdout}\n{stderr}"
            if execute.returncode > 0:
                output = f"{output}\nProcess exited with code {execute.returncode}"
            return output
        else:
            return "No output produced."
    except subprocess.SubprocessError as err:
        return f"Error: executing Python file: {err}"
