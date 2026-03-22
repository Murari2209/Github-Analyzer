import os
import subprocess
import streamlit as st
from src.api_collector import fetch_repositories
from src.data_cleaner import clean_data
from src.analyzer import add_features, rank_repositories
import pandas as pd


st.title("GitHub Developer Analytics Platform")

st.set_page_config(page_title="GitHub Analytics", layout="wide")

if st.button("Refresh Data"):
   st.cache_data.clear()
   st.rerun()
   st.success("Fetching latest data ...")
@st.cache_data(ttl=60)
def load_data():
    df = fetch_repositories()
    clean_df = clean_data("data/raw_repos.csv")
    featured_df = add_features(clean_df)
    ranked_df = rank_repositories(featured_df)
    return ranked_df

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Top Programming Languages")
st.bar_chart(df["language"].value_counts().head(5)) 

st.subheader("Top Repositories")
top_repos = df.sort_values(by="score", ascending=False).head(10)
st.dataframe(top_repos)

st.sidebar.header("Filters")

selected_language = st.sidebar.selectbox(
    "Select Language",
    options=df["language"].dropna().unique()
)

filtered_df = df[df["language"] == selected_language]

st.subheader(f"Repositories in {selected_language}")

st.dataframe(filtered_df.head(10))