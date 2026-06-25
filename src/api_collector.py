import streamlit as st
import pandas as pd
import datetime
from src.github_api import github_error_message, github_get_with_auth_fallback

today = datetime.date.today()
last_week = today - datetime.timedelta(days=7)


def _is_streamlit_app():
    try:
        from streamlit.runtime.scriptrunner_utils.script_run_context import (
            get_script_run_ctx,
        )

        return get_script_run_ctx(suppress_warning=True) is not None
    except Exception:
        return False


def _show_warning(message):
    if _is_streamlit_app():
        st.warning(message)
    else:
        print(f"Warning: {message}")


def _show_error(message):
    if _is_streamlit_app():
        st.error(message)
    else:
        print(f"Error: {message}")


def fetch_repositories(topic="python", max_pages=2):
    all_repos = []
    auth_warning_shown = False

    for page in range(1, max_pages + 1):
        url = "https://api.github.com/search/repositories"

        params = {
            "q": f"{topic} created:>{last_week}",
            "sort": "stars",
            "order": "desc",
            "per_page": 50,
            "page": page
        }

        response, used_auth, auth_retried = github_get_with_auth_fallback(
            url,
            params=params,
        )

        

        if response.status_code != 200:
            _show_error(
                github_error_message(
                    response,
                    "Failed to fetch trending repositories",
                    used_auth=used_auth,
                    auth_retried=auth_retried,
                )
            )
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
