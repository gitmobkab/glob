import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write/Create the specified content in the file specified via path (relative to the working directory), the provided content will fully override any previous one",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the file path to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "the content to write into the file",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_file_is_valid = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not target_file_is_valid:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parents = os.path.dirname(target_file)
        os.makedirs(parents, exist_ok=True)
        with open(target_file, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as err:
        return f'Error: "{err}"'
