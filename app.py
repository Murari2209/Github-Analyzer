import os
import subprocess
import streamlit as st
import pandas as pd

st.title("GitHub Developer Analytics Platform")

st.set_page_config(page_title="GitHub Analytics", layout="wide")

file_path = "data/processed_repos.csv"
if not os.path.exists(file_path):
  st.info("Fetching data from Github..... Please Wait..")

  try:
    subprocess.run(["python", "main.py"], check=True)

  except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

df = pd.read_csv("data/processed_repos.csv")

st.write("Dataset Preview")
st.dataframe(df.head())

st.subheader("Top Programming Languages")

lang_counts = df["language"].value_counts()

st.bar_chart(lang_counts)

st.subheader("Top Ranked Repositories")

top_repos = df.sort_values(by="score", ascending=False).head(10)

st.dataframe(top_repos[["name", "stars", "forks", "score"]])


st.sidebar.header("Filters")

selected_language = st.sidebar.selectbox(
    "Select Language",
    options=df["language"].dropna().unique()
)

filtered_df = df[df["language"] == selected_language]

st.subheader(f"Repositories in {selected_language}")

st.dataframe(filtered_df.head(10))