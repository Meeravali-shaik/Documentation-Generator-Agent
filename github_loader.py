import os
import tempfile
import shutil
import zipfile
import requests
import re

def clone_repo(repo_url):
    """
    Download a GitHub repository using the GitHub API.
    On Vercel (and other serverless platforms), git CLI is not available,
    so we download the repository as a zip file instead.
    
    Supports:
    - https://github.com/user/repo
    - https://github.com/user/repo.git
    - github.com/user/repo
    """
    try:
        # Parse the GitHub URL
        repo_url = repo_url.rstrip('/')
        
        # Extract owner and repo name
        match = re.search(r'github\.com[:/](.+?)/(.+?)(?:\.git)?$', repo_url)
        if not match:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")
        
        owner, repo_name = match.groups()
        repo_name = repo_name.replace('.git', '')
        
        # Use system temp directory (writable on Vercel and other serverless platforms)
        temp_base = tempfile.gettempdir()
        target_path = os.path.join(temp_base, "doc_gen", repo_name)

        # Clean up old clone if it exists
        if os.path.exists(target_path):
            try:
                shutil.rmtree(target_path)
            except Exception as e:
                print(f"Warning: Could not remove old repo: {e}")

        # Create directory
        os.makedirs(target_path, exist_ok=True)

        # Download repository as zip from GitHub API
        download_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
        
        print(f"Downloading {owner}/{repo_name} from GitHub...")
        response = requests.get(download_url, timeout=30, stream=True)
        
        # Try master branch if main doesn't exist
        if response.status_code == 404:
            download_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/master.zip"
            response = requests.get(download_url, timeout=30, stream=True)
        
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code}. Repository may not exist.")
        
        # Save zip file
        zip_path = os.path.join(temp_base, f"{repo_name}.zip")
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_path)
        
        # Remove zip file
        os.remove(zip_path)
        
        # The extracted folder has a name like "repo-main" or "repo-master"
        # Find the actual extracted directory
        extracted_dirs = os.listdir(target_path)
        if len(extracted_dirs) == 1:
            extracted_path = os.path.join(target_path, extracted_dirs[0])
            # Move contents up one level
            for item in os.listdir(extracted_path):
                src = os.path.join(extracted_path, item)
                dst = os.path.join(target_path, item)
                shutil.move(src, dst)
            shutil.rmtree(extracted_path)
        
        print(f"Successfully downloaded {repo_name}")
        return target_path

    except Exception as e:
        raise Exception(f"Failed to download repository: {str(e)}")

