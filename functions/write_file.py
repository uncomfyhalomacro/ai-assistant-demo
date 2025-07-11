import os
import functools
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file. If the file exists, overwrite the file, otherwise create it. Files are constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write onto the file. Empty content is a valid value.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    joined_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if joined_file_path == working_directory:
        return f'Error: Cannot write "{file_path}" as it points to a directory.'
    if not joined_file_path.startswith(working_directory):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(joined_file_path):
        path_segments = joined_file_path.split("/")
        _last_path_segment = path_segments.pop()
        reconstructed_path_segments = "/" + functools.reduce(
            os.path.join, path_segments
        )
        os.makedirs(reconstructed_path_segments, exist_ok=True)

    with open(joined_file_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
