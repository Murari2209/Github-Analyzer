import streamlit as st
import pandas as pd

st.title("GitHub Developer Analytics Dashboard")

df = pd.read_csv("data/processed_repos.csv")

st.write("Dataset Preview")
st.dataframe(df.head())