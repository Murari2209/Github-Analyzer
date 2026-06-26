import streamlit as st


def render_hero():

    st.markdown("""
    <style>

    .main-title{
        text-align:center;
        font-size:45px;
        font-weight:600;
        color:white;
        margin-top:10px;
    }

    .sub-title{
        text-align:center;
        font-size:20px;
        color:#9CA3AF;
        margin-bottom:35px;
    }

    .hero-box{
        background:#0F172A;
        border:1px solid #1E293B;
        border-radius:18px;
        padding:20px;
        box-shadow:0px 5px 30px rgba(0,0,0,.25);
    }

    .stTextInput input{
        border-radius:12px;
        font-size:18px;
    }

    div.stButton>button{
        height:50px;
        width:100%;
        top-margin:10px;
        border-radius:12px;
        background:#2563EB;
        color:white;
        font-size:18px;
        font-weight:400;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
    🤖 AI GitHub Developer Analyzer
    </div>

    <div class="sub-title">
    Analyze GitHub developers using AI, evaluate skills, projects and generate professional reports.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([5,1])

    with c1:
        username = st.text_input(
            "",
            placeholder="Enter GitHub username..."
        )

    with c2:
        st.write("")
        analyze = st.button("🚀 Analyze")

    st.markdown("</div>", unsafe_allow_html=True)

    return username, analyze