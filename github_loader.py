import os
import subprocess

def clone_repo(repo_url):
    folder_name = repo_url.split("/")[-1].replace(".git", "")
    target_path = os.path.join("temp_repo", folder_name)

    os.makedirs("temp_repo", exist_ok=True)

    if os.path.exists(target_path):
        subprocess.run(["git", "-C", target_path, "pull"], check=True)
    else:
        subprocess.run(["git", "clone", repo_url, target_path], check=True)

    return target_path
