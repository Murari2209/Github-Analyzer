# 🚀 GitHub Developer Analytics Platform

A production-style Python project that collects repository data from GitHub, processes it through a data pipeline, ranks repositories using a custom scoring algorithm, and visualizes insights via an interactive dashboard.

---

## 📌 Features

- 🔗 GitHub API integration with authentication
- 📊 Data pipeline (collection → cleaning → transformation)
- 🧠 Feature engineering (repo age, stars/day)
- 🏆 Repository ranking algorithm
- 📈 Interactive dashboard using Streamlit
- ⚙️ Backend API using FastAPI
- 🔐 Secure token handling using environment variables

---

## 🧱 Tech Stack

- Python
- Pandas
- Streamlit
- FastAPI
- Requests
- Matplotlib
- Python-dotenv
- GitHub REST API

---

## 📂 Project Structure
github-analytics-platform/

data/
raw_repos.csv
processed_repos.csv

src/
api_collector.py
data_cleaner.py
analyzer.py
visualizer.py
api_server.py

charts/

app.py
main.py
requirements.txt
README.md
.env (not pushed to GitHub)


## Create Virtual Environment

python -m venv venv
venv\Scripts\activate


## install dependencies
pip install -r requirements.txt


## Add Github Token 
Create `.env` file in root:

GITHUB_TOKEN = "Github token"


## How to Run

# Step 1 — Run Data Pipeline
python main.py

## Step 2 — Run Dashboard
streamlit run app.py

##  Dashboard Features

Top programming languages
Top ranked repositories
Filtering by language
Repository insights


##  Author

Murari Shrivastava

