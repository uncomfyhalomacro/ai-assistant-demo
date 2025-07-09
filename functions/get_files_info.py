import os


def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    joined_directory = os.path.abspath(os.path.join(working_directory, directory))
    what_dir = "current" if working_directory == joined_directory else f"'{directory}'"
    if not joined_directory.startswith(working_directory):
        return f'Result for {what_dir} directory:\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(joined_directory):
        return f'Result for {what_dir} path:\n    Error: "{directory}" is not a directory'
    listdir = os.listdir(joined_directory)
    metadata_dict = dict([(f, {"file_size": os.path.getsize(os.path.join(joined_directory, f)), "is_dir": os.path.isdir(os.path.join(joined_directory,f))}) for f in listdir])
    output_list = build_output_metadata_list(metadata_dict)
    output_list = [f" {item}" for item in output_list]
    return f"Result for {what_dir} directory:\n"+ "\n".join(output_list)


def build_output_metadata_list(metadata):
    if not isinstance(metadata, dict):
        raise TypeError("Error: metadata should be a dictionary")

    output=[]
    for (f, meta) in metadata.items():
        meta_str = process_meta(**meta)
        output.append(f"- {f}: {meta_str}")
    return output

def process_meta(**kwargs):
    file_size, is_dir = kwargs["file_size"], kwargs["is_dir"]
    return f"file_size={file_size} bytes, is_dir={is_dir}"
    

