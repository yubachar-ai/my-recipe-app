import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stButton>button {
            border-radius: 20px;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #ff3333;
            transform: scale(1.02);
        }
        .recipe-card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border-right: 5px solid #FF4B4B;
            direction: rtl;
            text-align: right;
            white-space: pre-line;
        }
        h1 { color: #2e3b4e; text-align: right; }
        </style>
        """, unsafe_allow_html=True)