from src.github_api import github_error_message, github_get_with_auth_fallback


def fetch_github_data(username):
    base_url = "https://api.github.com/users"

    try:
        profile_res, used_auth, auth_retried = github_get_with_auth_fallback(
            f"{base_url}/{username}"
        )

        if profile_res.status_code != 200:
            return (
                None,
                None,
                github_error_message(
                    profile_res,
                    "GitHub user lookup failed",
                    used_auth=used_auth,
                    auth_retried=auth_retried,
                ),
            )

        profile = profile_res.json()

        repos_res, used_auth, auth_retried = github_get_with_auth_fallback(
            f"{base_url}/{username}/repos",
            params={"per_page": 100},
        )

        if repos_res.status_code != 200:
            return (
                profile,
                None,
                github_error_message(
                    repos_res,
                    "Failed to fetch repositories",
                    used_auth=used_auth,
                    auth_retried=auth_retried,
                ),
            )

        repos = repos_res.json()

        return profile, repos, None

    except Exception as e:
        return None, None, str(e)


def calculate_developer_score(profile, repos):

    score = 0

    # Public repositories (max 25 points)
    score += min(profile.get("public_repos", 0), 25)

    # Followers (max 20 points)
    score += min(profile.get("followers", 0) // 5, 20)

    # Languages diversity (max 15 points)
    languages = set()

    for repo in repos:
        if repo.get("language"):
            languages.add(repo.get("language"))

    score += min(len(languages) * 3, 15)

    # Stars (max 25 points)
    total_stars = sum(
        repo.get("stargazers_count", 0)
        for repo in repos
    )

    score += min(total_stars, 25)

    # Profile completeness (max 15 points)
    completeness = 0

    if profile.get("bio"):
        completeness += 5

    if profile.get("location"):
        completeness += 5

    if profile.get("blog"):
        completeness += 5

    score += completeness

    return min(score, 100)