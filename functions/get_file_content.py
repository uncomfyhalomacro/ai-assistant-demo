import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content from a specified path to a file, if such a file exists and is constrained to the working directory.",
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

MAX_CHARS = 10000


def get_file_content(working_directory, file_path=None):
    if not file_path:
        return "Error: File to get content was not specified."
    working_directory = os.path.abspath(working_directory)
    joined_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    what_file = "current" if working_directory == joined_file_path else f"'{file_path}'"
    if not joined_file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(joined_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    byte_length = os.path.getsize(joined_file_path)
    with open(joined_file_path, "r") as f:
        content = f.read(MAX_CHARS)
        if byte_length > MAX_CHARS:
            content + '[...File "{file_path}" truncated at 10000 characters]'
        return content
    return "Error: Failed to read file"
