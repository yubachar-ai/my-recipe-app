import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Assistant:wght@300;400;600&display=swap');

    .stApp { background-color: #F9F7F2; }
    header, footer, [data-testid="stHeader"] {display: none !important;}

    /* מבנה הספר */
    .swiper { width: 100%; height: 85vh; padding-top: 20px; }
    
    .swiper-slide {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .book-cover {
        background-color: #556B2F;
        color: white;
        width: 320px;
        height: 500px;
        border-radius: 5px 15px 15px 5px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 15px 15px 30px rgba(0,0,0,0.2);
        border-left: 10px solid #3e4f22;
    }

    .recipe-page {
        background: white;
        width: 90%;
        max-width: 450px;
        height: 600px;
        padding: 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-radius: 2px;
        direction: rtl;
        text-align: right;
        overflow-y: auto;
    }
    </style>
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    """, unsafe_allow_html=True)
