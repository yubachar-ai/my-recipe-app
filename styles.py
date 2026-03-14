import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    .stApp { background-color: #F9F7F2; direction: rtl; }
    header, footer, [data-testid="stHeader"] {display: none !important;}

    /* עיצוב הטאבים (הפרקים בספר) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 1px solid #E8E4D8;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-family: 'Assistant', sans-serif;
        color: #556B2F;
    }

    .stTabs [aria-selected="true"] {
        background-color: #556B2F !important;
        color: white !important;
        border-color: #556B2F !important;
    }

    /* דף המתכון */
    .recipe-page {
        background: white;
        padding: 60px 40px;
        max-width: 800px;
        margin: 0 auto;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.05);
        border-right: 10px solid #556B2F;
        text-align: right;
    }

    h1, h2 { font-family: 'Playfair Display', serif !important; color: #2D2926; }
    </style>
    """, unsafe_allow_html=True)
