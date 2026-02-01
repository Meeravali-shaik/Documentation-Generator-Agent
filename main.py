from repo_parser import read_repo
from ast_analyzer import analyze_python
from llm_agent import generate_doc
from markdown_writer import write_markdown
from dependency_graph import create_graph
from github_loader import clone_repo
import os



choice = input("Enter 1 for local folder, 2 for GitHub repo: ")

if choice == "1":
    REPO_PATH = input("Enter local folder path: ")
else:
    repo_url = input("Enter GitHub repo URL: ")
    REPO_PATH = clone_repo(repo_url)



files = read_repo(REPO_PATH)
dependencies = {}   

for path, code in files.items():
    print(f"Processing: {path}")

    try:
        funcs, calls = analyze_python(code)
        dependencies[path] = calls
    except:
        dependencies[path] = []

  
    doc, meta = generate_doc(code[:12000])

    name = os.path.basename(path).replace(".py", "")
    write_markdown(name, doc)

    with open("docs/compression_report.txt", "a", encoding="utf-8") as f:
        f.write(f"{name}\n{str(meta)}\n\n")



create_graph(dependencies)

print(" Documentation Generated in /docs")
