import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN").strip()

print("Token:", token[:10])

r = requests.get(
    "https://api.github.com/users/octocat",
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
)

print("token repr:", repr(token))
print("length:", len(token))