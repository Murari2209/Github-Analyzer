import streamlit as st


def render_ai_analysis(ai_analysis):

    st.markdown("""
    <style>

    .ai-card{
        background:linear-gradient(135deg,#111827,#1F2937);
        border-radius:20px;
        padding:30px;
        border:1px solid #374151;
        margin-top:25px;
        margin-bottom:25px;
    }

    .ai-title{
        color:white;
        font-size:28px;
        font-weight:700;
        margin-bottom:20px;
    }

    .ai-content{
        color:#E5E7EB;
        font-size:16px;
        line-height:1.8;
        white-space:pre-wrap;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-card">
        <div class="ai-title">
            🤖 AI Developer Assessment
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="ai-content">{ai_analysis}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)