from functions.run_python_file import run_python_file

cwd = "calculator"

tests : list[dict] = [
    {"file": "main.py"},
    {"file": "main.py", "args": ["3 + 5"]},
    {"file": "tests.py"},
    {"file": "../main.py"},
    {"file": "nonexistent.py"},
    {"file": "lorem.txt"},
]

for i, test in enumerate(tests, 1):
    file = test["file"]
    args = test.get("args", [])
    result = run_python_file(cwd, file, args)
    print(f"--------<Test {i}>------------")
    print(result)
    print(f"--------<\\Test {i}>------------\n")