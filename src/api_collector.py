import requests
import pandas as pd

def fetch_repositories(topic="python", pages=2):

    repos = []

    for page in range(1, pages + 1):

        url = f"https://api.github.com/search/repositories?q=topic:{topic}&page={page}"

        response = requests.get(url)

        data = response.json()

        for repo in data["items"]:

            repos.append({
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"],
                "created_at": repo["created_at"]
            })

    df = pd.DataFrame(repos)

    df.to_csv("data/raw_repos.csv", index=False)

    return df