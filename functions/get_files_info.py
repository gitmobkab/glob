import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        target_dir_is_valid = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not target_dir_is_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        files_info = list_dir(target_dir)
        formatted_infos = list(map(format_file_info, files_info))
        return "\n".join(formatted_infos)
    except Exception as err:
        return f'Error: "{err}"'

def list_dir(abs_dir: str) -> list[dict]:
    files = []
    for file in os.listdir(abs_dir):
        abs_file = os.path.join(abs_dir, file)
        file_info = {
            "name": file,
            "size": os.path.getsize(abs_file),
            "is_dir": os.path.isdir(abs_file),
        }

        files.append(file_info)
    return files    

def format_file_info(file_info: dict) -> str:
    return f"- {file_info['name']}: file_size={file_info['size']} bytes, is_dir={file_info['is_dir']}"
