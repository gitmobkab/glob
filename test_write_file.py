from functions.write_file import write_file

working_dir = "calculator"

tests = [
    {
        "file": "lorem.txt",
        "content": "wait, this isn't lorem ipsum",
    },
    {
        "file": "pkg/morelorem.txt",
        "content": "lorem ipsum dolor sit amet",
    },
    {
        "file": "/tmp/temp.txt",
        "content": "this should not be allowed",
    },
]

for test in tests:
    result = write_file(working_dir, test["file"], test["content"])
    print(result)