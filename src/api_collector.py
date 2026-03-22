import requests
import os
import streamlit as st
import pandas as pd

def fetch_repositories(topic="python", max_pages=2):

    token = os.getenv("GITHUB_TOKEN") or st.secrets.get("GITHUB_TOKEN")

    if not token:
        raise Exception("GitHub token not found")

    headers = {
        "Authorization": f"token {token}"
    }

    all_repos = []

    for page in range(1, max_pages + 1):
        url = "https://api.github.com/search/repositories"

        params = {
            "q": topic,
            "sort": "stars",
            "order": "desc",
            "per_page": 50,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)

        # ✅ Handle API failure
        if response.status_code != 200:
            st.error(f"GitHub API Error: {response.status_code}")
            return pd.DataFrame()

        data = response.json()

        items = data.get("items", [])

        if not items:
            break

        for repo in items:
            all_repos.append({
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"],
                "created_at": repo["created_at"]
            })

    # ✅ IMPORTANT: Handle empty data safely
    if len(all_repos) == 0:
        return pd.DataFrame()

    return pd.DataFrame(all_repos)