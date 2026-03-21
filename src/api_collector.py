import os
import requests
import pandas as pd
import time

BASE_URL = "https://api.github.com/search/repositories"


def fetch_repositories(topic="python", max_pages=5):

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise Exception("GitHub token not found. Set GITHUB_TOKEN.")

    headers = {
        "Authorization": f"token {token}"
    }

    repos = []

    for page in range(1, max_pages + 1):

        params = {
            "q": f"topic:{topic}",
            "page": page,
            "per_page": 30
        }

        try:
            response = requests.get(BASE_URL, headers=headers, params=params)

            # 🔍 Check status
            if response.status_code == 200:

                data = response.json()

                for repo in data.get("items", []):
                    repos.append({
                        "name": repo["name"],
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"],
                        "language": repo["language"],
                        "created_at": repo["created_at"]
                    })

                print(f"Page {page} fetched successfully")

            elif response.status_code == 403:
                print("Rate limit hit. Sleeping for 60 seconds...")
                time.sleep(60)
                continue

            else:
                print(f"Error: {response.status_code}")
                continue

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            continue

        # ⏱️ Small delay (good practice)
        time.sleep(1)

    df = pd.DataFrame(repos)

    df.to_csv("data/raw_repos.csv", index=False)

    return df