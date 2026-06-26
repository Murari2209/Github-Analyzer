import os
import subprocess
import streamlit as st
from components.hero import render_hero
from github_service import fetch_github_data,calculate_developer_score
from pdf_service import generate_pdf
from src.api_collector import fetch_repositories
from src.data_cleaner import clean_data
from src.analyzer import add_features, rank_repositories
from ai_service import analyze_developer
from components.profile_card import render_profile_card
from components.metric_cards import render_metric_cards
from components.ai_analysis import render_ai_analysis
import pandas as pd

st.set_page_config(
    page_title="AI GitHub Developer Analyzer",
    page_icon="🤖",
    layout="wide",
)

username, analyze_btn = render_hero()

def _profile_snapshot(profile):
    keys = ("login", "name", "bio", "followers", "public_repos", "html_url")
    return tuple((key, profile.get(key)) for key in keys)


def _repo_snapshot(repos):
    keys = ("name", "language", "stargazers_count", "forks_count")
    return tuple(
        tuple((key, repo.get(key)) for key in keys)
        for repo in repos[:50]
    )


@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_ai_analysis(profile_snapshot, repo_snapshot):
    profile = dict(profile_snapshot)
    repos = [dict(repo) for repo in repo_snapshot]
    return analyze_developer(profile, repos)

if analyze_btn and username:
    profile, repos, error = fetch_github_data(username.strip())
    developer_score = calculate_developer_score(profile, repos)
    
    render_metric_cards(
     profile,
     repos,
     developer_score
  )

    if error:
        st.error(error)
        st.stop()

    if repos is None:
     st.error("Failed to fetch repositories")
     st.stop()

    if len(repos) == 0:
     st.warning("No repositories found")
     ai_analysis = "No repository data available for analysis."
    else:
     st.success("Data fetched successfully")
     with st.spinner("🤖 AI is analyzing developer profile..."):
      ai_analysis = get_cached_ai_analysis(
          _profile_snapshot(profile),
          _repo_snapshot(repos),
      )
    pdf_file = generate_pdf(
       profile,
       repos,
       ai_analysis)
    
    st.write(f"Total repos: {len(repos)}")
    render_profile_card(profile, developer_score)

    
    render_ai_analysis(ai_analysis)
    
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name=f"{profile['login']}_developer_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
        
        

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
