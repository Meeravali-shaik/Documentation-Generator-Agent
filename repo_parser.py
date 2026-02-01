import os

def read_repo(path):
    code_files = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java")):
                fp = os.path.join(root, file)
                with open(fp, "r", encoding="utf-8") as f:
                    code_files[fp] = f.read()
    return code_files
