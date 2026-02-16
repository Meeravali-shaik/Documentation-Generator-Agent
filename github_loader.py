import os
import subprocess
import tempfile
import shutil

def clone_repo(repo_url):
    """
    Clone a GitHub repository to a temporary directory.
    On Vercel (and other serverless platforms), only /tmp is writable.
    """
    try:
        folder_name = repo_url.split("/")[-1].replace(".git", "")
        
        # Use system temp directory (/tmp on Linux, system temp on Windows)
        # This is writable on Vercel and other serverless platforms
        temp_base = tempfile.gettempdir()
        target_path = os.path.join(temp_base, "doc_gen", folder_name)

        # Clean up old clone if it exists
        if os.path.exists(target_path):
            try:
                shutil.rmtree(target_path)
            except Exception as e:
                print(f"Warning: Could not remove old repo: {e}")

        # Create directory
        os.makedirs(target_path, exist_ok=True)

        # Clone the repository
        result = subprocess.run(
            ["git", "clone", repo_url, target_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            raise Exception(f"Git clone failed: {result.stderr}")

        return target_path

    except Exception as e:
        raise Exception(f"Failed to clone repository: {str(e)}")
