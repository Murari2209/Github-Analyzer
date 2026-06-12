import os
import subprocess
import streamlit as st
from github_service import fetch_github_data
from src.api_collector import fetch_repositories
from src.data_cleaner import clean_data
from src.analyzer import add_features, rank_repositories

from ai_service import analyze_developer
import pandas as pd


st.set_page_config(page_title="GitHub Analytics", layout="wide")
st.title("GitHub Developer Analytics Platform")


st.subheader("🔍 Analyze GitHub Developer")

col1, col2 = st.columns([4, 2])

with col1:
    username = st.text_input("Enter GitHub Username")

with col2:
    analyze_btn = st.button("Analyze")

if analyze_btn and username:
    profile, repos, error = fetch_github_data(username)

    if error:
        st.error(error)
        st.stop()

    if repos is None:
     st.error("Failed to fetch repositories")
     st.stop()

    if len(repos) == 0:
     st.warning("No repositories found")
    else:
     st.success("Data fetched successfully")
     with st.spinner("🤖 AI is analyzing developer profile..."):
      ai_analysis = analyze_developer(profile, repos)
     st.write(f"Total repos: {len(repos)}")

    col1, col2 = st.columns([1, 3])

    with col1:
     st.image(profile["avatar_url"], width=120)

    with col2:
     st.markdown(f"### {profile.get('name') or profile.get('login')}")
     st.markdown(f"**Bio:** {profile.get('bio') or 'No bio'}")
     st.markdown(f"🔗 [GitHub Profile]({profile.get('html_url')})")

     st.markdown("---")

     st.subheader("🤖 AI Developer Analysis")

     st.markdown(ai_analysis)
    
    

if st.button("Refresh Data"):
   st.cache_data.clear()
   st.rerun()
   st.success("Fetching latest data ...")

@st.cache_data(ttl=60)
def load_data():
    df = fetch_repositories()
    if df.empty:
        return df
    clean_df = clean_data(df)
    featured_df = add_features(clean_df)
    ranked_df = rank_repositories(featured_df)
    return ranked_df

df = load_data()

if df.empty:
    st.error("No data available. Please try again later.")
    st.stop()

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