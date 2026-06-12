import requests
import os


def fetch_github_data(username):
    base_url = "https://api.github.com/users"

    headers = {
        "Accept": "application/vnd.github+json",
        # Optional (recommended to avoid rate limits):
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
    }

    try:
        # 🔹 Profile request
        profile_res = requests.get(f"{base_url}/{username}", headers=headers)

        if profile_res.status_code != 200:
            return None, None, f"User not found or API error ({profile_res.status_code})"

        profile = profile_res.json()

        # 🔹 Repo request
        repos_res = requests.get(f"{base_url}/{username}/repos?per_page=100", headers=headers)

        if repos_res.status_code != 200:
            return profile, None, "Failed to fetch repos"

        repos = repos_res.json()

        return profile, repos, None

    except Exception as e:
        return None, None, str(e)