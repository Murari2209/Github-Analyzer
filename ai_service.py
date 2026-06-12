import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_developer(profile, repos):

    prompt = f"""
    Analyze this GitHub developer:

    Name: {profile.get('name')}
    Bio: {profile.get('bio')}
    Followers: {profile.get('followers')}
    Public Repositories: {profile.get('public_repos')}

    Repositories:
    {[repo['name'] for repo in repos[:10]]}

    Languages:
    {list(set([repo.get('language') for repo in repos if repo.get('language')]))}

    Give:
    1. Skill Level
    2. Strengths
    3. Industry Fit
    4. Improvement Suggestions

    Format the response nicely.
    """

    response = model.generate_content(prompt)

    return response.text