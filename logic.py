import google.generativeai as genai
import streamlit as st
from streamlit_gsheets import GSheetsConnection

def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-3-flash-preview')

def save_recipe_to_cloud(user_email, name, content, category):
    # החיבור משתמש אוטומטית ב-Secrets שהגדרנו תחת [connections.gsheets]
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read() # הוא כבר יודע איזה גיליון לקרוא מה-Secrets
    
    new_data = {"user": user_email, "name": name, "category": category, "content": content}
    
    # הוספה ועדכון
    updated_df = df.append(new_data, ignore_index=True)
    conn.update(data=updated_df)

def load_recipes_from_cloud(user_email):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    return df[df['user'] == user_email]
