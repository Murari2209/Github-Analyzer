import pandas as pd

def clean_data(file_path):

    df = pd.read_csv(file_path)

    df = df.dropna()

    df["created_at"] = pd.to_datetime(df["created_at"])

    return df