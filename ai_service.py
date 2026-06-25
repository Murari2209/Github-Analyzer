import google.generativeai as genai
import os
import re
from collections import Counter
from dotenv import load_dotenv

load_dotenv()


def _get_secret(name):
    try:
        import streamlit as st

        return os.getenv(name) or st.secrets.get(name)
    except Exception:
        return os.getenv(name)


def _repo_number(repo, field):
    value = repo.get(field) or 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _skill_level(profile, repos, total_stars):
    followers = _repo_number(profile, "followers")
    public_repos = _repo_number(profile, "public_repos") or len(repos)

    if total_stars >= 100 or followers >= 50 or public_repos >= 30:
        return "Advanced / portfolio-ready"

    if total_stars >= 20 or followers >= 10 or public_repos >= 8:
        return "Intermediate"

    return "Emerging"


def _quota_retry_text(message):
    retry_match = re.search(r"retry(?: in)? ([\d.]+)s", message, re.IGNORECASE)
    seconds_match = re.search(r"retry_delay \{ seconds: (\d+) \}", message)

    if retry_match:
        return f" Try again in about {round(float(retry_match.group(1)))} seconds."

    if seconds_match:
        return f" Try again in about {seconds_match.group(1)} seconds."

    return " Try again in a minute, or switch to a paid/quota-enabled Gemini key."


def _fallback_developer_analysis(profile, repos, note):
    languages = Counter(
        repo.get("language") for repo in repos if repo.get("language")
    )
    total_stars = sum(_repo_number(repo, "stargazers_count") for repo in repos)
    total_forks = sum(_repo_number(repo, "forks_count") for repo in repos)
    top_repos = sorted(
        repos,
        key=lambda repo: _repo_number(repo, "stargazers_count"),
        reverse=True,
    )[:5]

    language_summary = (
        ", ".join(language for language, _ in languages.most_common(5))
        if languages
        else "No dominant language detected"
    )
    repo_summary = (
        ", ".join(repo.get("name", "Unnamed repo") for repo in top_repos)
        if top_repos
        else "No public repositories found"
    )

    return f"""
**AI quota notice:** {note}

### Local Developer Analysis

**Skill Level:** {_skill_level(profile, repos, total_stars)}

**Strengths:**
- Public repositories analyzed: {len(repos)}
- Total stars across analyzed repos: {total_stars}
- Total forks across analyzed repos: {total_forks}
- Main languages: {language_summary}
- Notable repositories: {repo_summary}

**Industry Fit:**
This profile looks most aligned with roles or projects using {language_summary}.
Repository activity and public project variety are useful signals for portfolio review.

**Improvement Suggestions:**
- Pin or highlight the strongest repositories on GitHub.
- Add clear READMEs, screenshots, setup steps, and project outcomes.
- Add tests or CI badges to make projects look more production-ready.
- Keep working on a few polished projects instead of only many small experiments.
"""


def analyze_developer(profile, repos):
    api_key = (_get_secret("GEMINI_API_KEY") or "").strip().strip("\"'")

    if not api_key:
        return _fallback_developer_analysis(
            profile,
            repos,
            "GEMINI_API_KEY is missing, so this section is using local analysis.",
        )

    genai.configure(api_key=api_key)
    model_name = (os.getenv("GEMINI_MODEL") or "gemini-2.5-flash").strip()
    model = genai.GenerativeModel(model_name)

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

    try:
        print("Calling Gemini...")
        response = model.generate_content(prompt)
        print("Gemini response:")
    except Exception as exc:
        message = str(exc)

        if "429" in message or "quota" in message.lower():
            return _fallback_developer_analysis(
                profile,
                repos,
                "Gemini quota was exceeded." + _quota_retry_text(message),
            )

        return _fallback_developer_analysis(
            profile,
            repos,
            "Gemini analysis is unavailable right now, so this section is using "
            "local analysis.",
        )

    return getattr(response, "text", None) or "AI analysis returned no text."
