import os

import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_API_VERSION = "2022-11-28"
REQUEST_TIMEOUT = 15

PLACEHOLDER_TOKENS = {
    "github token",
    "your github token",
    "your_github_token",
    "your-token-here",
    "github_token",
}


def _get_streamlit_secret(name):
    try:
        import streamlit as st

        return st.secrets.get(name)
    except Exception:
        return None


def get_github_token():
    token = os.getenv("GITHUB_TOKEN") or _get_streamlit_secret("GITHUB_TOKEN") or ""
    token = token.strip().strip("\"'")

    if not token or token.lower() in PLACEHOLDER_TOKENS:
        return None

    return token


def github_headers(include_auth=True):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }

    token = get_github_token()
    if include_auth and token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def github_get(url, *, params=None, include_auth=True):
    return requests.get(
        url,
        headers=github_headers(include_auth=include_auth),
        params=params,
        timeout=REQUEST_TIMEOUT,
    )


def github_get_with_auth_fallback(url, *, params=None):
    use_auth = get_github_token() is not None
    response = github_get(url, params=params, include_auth=use_auth)

    if response.status_code == 401 and use_auth:
        return github_get(url, params=params, include_auth=False), False, True

    return response, use_auth, False


def github_error_message(response, action, *, used_auth=True, auth_retried=False):
    try:
        message = response.json().get("message")
    except ValueError:
        message = response.text.strip()

    status_code = response.status_code
    details = f": {message}" if message else ""

    if status_code == 401 and used_auth:
        return (
            "GitHub API rejected GITHUB_TOKEN (401 Bad credentials). "
            "Update the token in .env, or remove GITHUB_TOKEN to use public "
            "unauthenticated requests."
        )

    if status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        return (
            "GitHub API rate limit exceeded. Add a valid GITHUB_TOKEN in .env "
            "and try again after the rate limit resets."
        )

    if status_code == 404:
        return f"{action}: not found (404)."

    retry_note = " after retrying without the rejected token" if auth_retried else ""
    return f"{action}: GitHub API error {status_code}{retry_note}{details}"
