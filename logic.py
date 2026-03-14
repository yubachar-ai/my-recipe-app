import google.generativeai as genai
import pandas as pd
import os

# הגדרת ה-AI
def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-3-flash-preview')

# הפרומפט שביקשת (נקי ומדויק)
RECIPE_PROMPT = """
תפקיד: מחלץ נתונים מקצועי מתמונות מתכונים.
המשימה: חלץ את המידע מהתמונה והחזר אותו בעברית לפי הפורמט הבא בלבד.

הנחיות קשיחות:
1. אל תוסיף הקדמות כמו "הנה המתכון" או סיכומים כמו "בתיאבון".
2. אל תוסיף טיפים, הערות או מידע שלא מופיע מפורשות בתמונה.
3. השורה הראשונה חייבת להיות שם המתכון בלבד.
4. השתמש בכותרות Markdown (סימן # לשם המתכון, ## למצרכים וכו').

פורמט פלט:
[שם המתכון]
### 🛒 מצרכים:
[רשימת המצרכים כפי שמופיעה]
### 👨‍🍳 הוראות הכנה:
[שלבי ההכנה כפי שמופיעים]
"""

def save_recipe_to_csv(name, content, category):
    file_name = 'my_recipes.csv'
    df_new = pd.DataFrame({'שם': [name], 'קטגוריה': [category], 'תוכן': [content]})
    if not os.path.isfile(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

def load_recipes():
    if os.path.isfile('my_recipes.csv'):
        return pd.read_csv('my_recipes.csv', encoding='utf-8-sig')
    return None