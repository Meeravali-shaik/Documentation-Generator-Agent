import os
import subprocess
import shutil

def clone_repo(repo_url):
    folder_name = repo_url.split("/")[-1].replace(".git", "")
    target_path = os.path.join("temp_repo", folder_name)

    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    os.makedirs("temp_repo", exist_ok=True)

    subprocess.run(["git", "clone", repo_url, target_path], check=True)

    return target_path
