from functions.get_file_content import get_file_content

working_dir = "calculator"

tests = [
    "main.py",
    "pkg/calculator.py",
    "/bin/cat",
    "pkg/does_not_exist.py"
]
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

for test in tests:
    result = get_file_content(working_dir, test)
    print(result)