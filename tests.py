from functions.get_files_info import get_files_info

tests = [
            {
                "wd": "calculator",
                "d": "."
            },
            {
                "wd": "calculator",
                "d": "pkg"
            },
            {
                "wd": "calculator",
                "d": "/bin"
            },
            {
                "wd": "calculator",
                "d": "../"
            },
        ]

for test in tests:
    print(get_files_info(test["wd"], test["d"]))
