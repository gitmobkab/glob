import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Print the content of a file relative to the working directory, the content of the file will be truncated if the characters exceed {MAX_CHARS} characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the file path to read, relative to the working directory (there's no default value)",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_file_is_valid = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not target_file_is_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as err:
        return f'Error: "{err}"'
