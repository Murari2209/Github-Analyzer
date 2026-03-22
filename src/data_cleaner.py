import pandas as pd

def clean_data(df):

    if df.empty:

        return df
    df = df.dropna(subset=["language"])
    df = df.drop_duplicates(subset=["name"])

    df["created_at"] = pd.to_datetime(df["created_at"])

    return df