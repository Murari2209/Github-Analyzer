import pandas as pd


# 🔹 Feature Engineering
def add_features(df):

    # Convert date
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Repo age in days
    df["repo_age_days"] = (pd.Timestamp.now() - df["created_at"]).dt.days

    # Stars per day (growth metric)
    df["stars_per_day"] = df["stars"] / (df["repo_age_days"] + 1)

    return df


# 🔹 Ranking Logic
def rank_repositories(df):

    df["score"] = (
        df["stars"] * 0.6 +
        df["forks"] * 0.3 +
        df["stars_per_day"] * 0.1
    )

    return df.sort_values(by="score", ascending=False)


# 🔹 Insights
def top_languages(df):
    return df["language"].value_counts().head(5)


def top_repositories(df):
    return df[["name", "stars", "forks", "score"]].head(10)