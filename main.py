from src.api_collector import fetch_repositories
from src.data_cleaner import clean_data
from src.visualizer import plot_languages
from src.analyzer import add_features, rank_repositories ,top_languages


df = fetch_repositories()

if df.empty:
    raise SystemExit("No repositories fetched from GitHub.")

df.to_csv("data/raw_repos.csv", index=False)

clean_df = clean_data(df)

lang_counts = top_languages(clean_df)

plot_languages(lang_counts)

featured_df = add_features(clean_df)
ranked_df = rank_repositories(featured_df)

ranked_df.to_csv("data/processed_repos.csv", index=False)
