import os

def write_markdown(title, content):
    os.makedirs("docs", exist_ok=True)
    with open(f"docs/{title}.md", "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}")
