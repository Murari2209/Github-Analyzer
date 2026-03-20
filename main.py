from src.api_collector import fetch_repositories
from src.data_cleaner import clean_data
from src.analyzer import language_distribution
from src.visualizer import plot_languages


df = fetch_repositories()

clean_df = clean_data("data/raw_repos.csv")

lang_counts = language_distribution(clean_df)

plot_languages(lang_counts)