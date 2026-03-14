import google.generativeai as genai
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-3-flash-preview')

RECIPE_PROMPT = """
תפקיד: מחלץ נתונים מקצועי.
הוראה: חלץ שם מתכון (שורה ראשונה), מצרכים והוראות. בלי תוספות.
"""

def save_recipe_to_cloud(user_email, name, content, category):
    url = st.secrets["GSHEETS_URL"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # קריאת הנתונים הקיימים
    df = conn.read(spreadsheet=url)
    
    # יצירת שורה חדשה
    new_data = pd.DataFrame({
        'user': [user_email],
        'name': [name],
        'category': [category],
        'content': [content]
    })
    
    # חיבור נתונים
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # שליחה לגוגל - כאן קרתה השגיאה
    # הוספנו את הפרמטר wait_to_finish כדי לוודא שזה נכתב
    conn.update(spreadsheet=url, data=updated_df)

def load_recipes_from_cloud(user_email):
    url = st.secrets["GSHEETS_URL"]
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url)
    return df[df['user'] == user_email]
