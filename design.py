import streamlit as st

def load_css():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Nastaliq Urdu', serif;
        direction: rtl;
        text-align: right;
    }

    .main-header{
        background: linear-gradient(90deg,#1e5631,#2e7d32);
        padding:25px;
        border-radius:10px;
        color:white;
        text-align:center;
        margin-bottom:20px;
    }

    .card{
        background:white;
        padding:20px;
        border-radius:12px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);
        text-align:center;
    }

    </style>
    """, unsafe_allow_html=True)
