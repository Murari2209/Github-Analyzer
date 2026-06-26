import streamlit as st


def render_profile_card(profile, repos):

    st.markdown("""
    <style>

    .profile-card{
        background: linear-gradient(135deg,#111827,#1F2937);
        padding:25px;
        border-radius:20px;
        border:1px solid #374151;
        margin-top:25px;
        margin-bottom:25px;
    }

    .profile-name{
        font-size:32px;
        font-weight:700;
        color:white;
    }

    .profile-bio{
        color:#D1D5DB;
        font-size:16px;
        margin-top:8px;
        margin-bottom:20px;
    }

    .metric-card{
        background:#0F172A;
        border-radius:12px;
        padding:12px;
        text-align:center;
        border:1px solid #334155;
    }

    .metric-title{
        color:#94A3B8;
        font-size:14px;
    }

    .metric-value{
        color:white;
        font-size:24px;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-card">', unsafe_allow_html=True)

    left, right = st.columns([1,3])

    with left:
        st.image(profile["avatar_url"], width=170)

    with right:

        st.markdown(
            f'<div class="profile-name">{profile.get("name") or profile.get("login")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="profile-bio">{profile.get("bio") or "No bio available."}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"📍 **Location:** {profile.get('location') or 'Not specified'}")

        with col2:
            st.markdown(f"🏢 **Company:** {profile.get('company') or 'Not specified'}")

            st.markdown(f"📅 **Joined GitHub:** {profile.get('created_at','')[:10]}")

            st.write("")

            st.link_button(
                "🌐 View GitHub Profile",
                profile["html_url"],
                use_container_width=True,
            )

            

    st.markdown("</div>", unsafe_allow_html=True)