import os
import subprocess

from config import RUN_TIMEOUT

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute the specified python file path relative to the working directory, scripts must end before a 30s timeout.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the file path to the python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "Additional args to pass to the script",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": ["file_path"]
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_file_is_valid = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not target_file_is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        exec_args = ["python", target_file]
        if args:
            exec_args.extend(args)
        
        run = subprocess.run(
            args=exec_args,
            cwd=working_directory,
            text=True,
            capture_output=True,
            timeout=RUN_TIMEOUT,
        )
        
        output : list[str] = []
        if run.returncode != 0:
            output.append(f"Process exited with code {run.returncode}")
        if run.stdout:
            output.append(f"STDOUT: {run.stdout}")
        if run.stderr:
            output.append(f"STDERR: {run.stderr}")
        return "\n".join(output)
    except Exception as err:
        return f'Error: executing python file: {err}'
