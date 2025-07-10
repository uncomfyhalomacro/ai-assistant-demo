import os
import functools


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

    if not os.path.isfile(joined_file_path):
        return f'Error: "{file_path}" is not a file.'
    with open(joined_file_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
