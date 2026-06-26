import streamlit as st


def render_metric_cards(profile, repos, developer_score):

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)

    st.markdown("""
    <style>

    .metric-box{
        background:linear-gradient(135deg,#111827,#1E293B);
        padding:22px;
        border-radius:18px;
        border:1px solid #334155;
        text-align:center;
        transition:0.3s;
    }

    .metric-box:hover{
        border:1px solid #2563EB;
    }

    .metric-icon{
        font-size:34px;
    }

    .metric-title{
        color:#9CA3AF;
        font-size:15px;
    }

    .metric-value{
        color:white;
        font-size:34px;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("🏆", "Developer Score", developer_score),
        ("👥", "Followers", profile.get("followers", 0)),
        ("📦", "Repositories", profile.get("public_repos", 0)),
        ("⭐", "Total Stars", total_stars),
    ]

    for col, card in zip([c1, c2, c3, c4], cards):
        icon, title, value = card

        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-icon">{icon}</div>
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)