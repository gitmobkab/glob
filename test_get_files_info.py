from functions.get_files_info import get_files_info

working_dir = "calculator"

tests_cases = [
    ".",
    "pkg",
    "/bin",
    "../"
]

for test in tests_cases:
    result = get_files_info(working_dir, test)
    header = f"Results for '{test}' directory"
    if test == ".":
        header = "Results for current directory"
    print("------------\n" + header)
    print(result)
    print("------------\n")
