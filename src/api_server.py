from fastapi import FastAPI
import pandas as pd

app = FastAPI()

DATA_PATH = "data/processed_repos.csv"


@app.get("/")
def home():
    return {"message": "GitHub Analytics API Running"}


@app.get("/top-repositories")
def top_repositories():

    df = pd.read_csv(DATA_PATH)

    top = df.sort_values(by="score", ascending=False).head(10)

    return top.to_dict(orient="records")


@app.get("/top-languages")
def top_languages():

    df = pd.read_csv(DATA_PATH)

    langs = df["language"].value_counts().head(5)

    return langs.to_dict()