import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Assistant:wght@300;400;600&display=swap');

    .stApp { background-color: #F9F7F2; }

    /* כריכת הספר */
    .book-cover {
        background-color: #556B2F;
        color: white;
        padding: 60px;
        border-radius: 5px 15px 15px 5px;
        box-shadow: 15px 15px 30px rgba(0,0,0,0.2);
        text-align: center;
        margin: 0 auto;
        max-width: 400px;
        border-left: 10px solid #3e4f22;
    }

    /* דף המתכון עם אנימציית דפדוף */
    .recipe-page {
        background: white;
        padding: 50px;
        max-width: 600px;
        margin: 0 auto;
        min-height: 700px;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.05);
        border-right: 1px solid #E8E4D8;
        direction: rtl;
        text-align: right;
        font-family: 'Assistant', sans-serif;
        animation: flipPage 0.6s ease-out;
    }

    @keyframes flipPage {
        from { transform: rotateY(-15deg) translateX(50px); opacity: 0.5; }
        to { transform: rotateY(0deg) translateX(0); opacity: 1; }
    }

    /* כפתורי דפדוף */
    .nav-button {
        background: transparent !important;
        border: 1px solid #556B2F !important;
        color: #556B2F !important;
        border-radius: 50% !important;
        width: 50px;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)
