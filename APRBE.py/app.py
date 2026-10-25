import streamlit as st
import ast
import json
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME CUSTOMIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Python Reviewer & Learning Hub",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signin"  # 'signin' or 'signup'
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "desktop_mode" not in st.session_state:
    st.session_state.desktop_mode = False
if "history" not in st.session_state:
    st.session_state.history = []
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Custom CSS styling based on theme
if st.session_state.theme == "Dark":
    bg_color = "#0e1117"
    card_bg = "#1e222a"
    text_color = "#ffffff"
else:
    bg_color = "#f0f2f6"
    card_bg = "#ffffff"
    text_color = "#1f2937"

st.markdown(f"""
    <style>
    .main {{ background-color: {bg_color}; color: {text_color}; }}
    .stApp {{ background-color: {bg_color}; }}
    .css-1r650q2, .css-12w0qpk {{ background-color: {card_bg} !important; }}
    .stCard {{
        background-color: {card_bg};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# Container width layout setting
if st.session_state.desktop_mode:
    st.markdown("""
        <style>
        .block-container {
            max-width: 1200px;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. AUTHENTICATION PAGE (SIGN IN / SIGN UP)
# -----------------------------------------------------------------------------
def render_auth():
    st.title("🐍 AI Python Code Reviewer & Learning Hub")
    st.subheader("Welcome! Please authenticate to continue.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        # --- TAB 1: SIGN IN ---
        with tab1:
            st.markdown("### Sign In")
            email = st.text_input("Email Address", key="signin_email")
            password = st.text_input("Password", type="password", key="signin_password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔓 Sign In", use_container_width=True):
                    if email and password:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error("Please enter email and password.")
            
            st.markdown("---")
            st.markdown("#### Or Sign In with Google")
            if st.button("🌐 Continue with Google Account", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_email = "user.google@gmail.com"
                st.rerun()

        # --- TAB 2: CREATE ACCOUNT ---
        with tab2:
            st.markdown("### Create New Account")
            new_email = st.text_input("Email Address", key="signup_email")
            new_password = st.text_input("Create Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("🚀 Register Account", use_container_width=True):
                if not new_email or not new_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    st.success("Account created successfully! Logging you in...")
                    st.session_state.authenticated = True
                    st.session_state.user_email = new_email
                    st.rerun()
                    
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. STATIC QUESTIONS GENERATOR (100 QUESTIONS)
# -----------------------------------------------------------------------------
def get_100_quiz_questions():
    questions = []
    # Generate 100 structured Python questions
    topics = ["Variables", "Data Types", "Lists", "Tuples", "Dictionaries", "Functions", "OOP", "Control Flow", "Modules", "Exceptions"]
    
    for i in range(1, 101):
        topic = topics[(i - 1) % len(topics)]
        questions.append({
            "id": i,
            "topic": topic,
            "question": f"Question {i} [{topic}]: What is the output or behavior of python expression evaluated for question #{i}?",
            "code": f"# Question {i} Example\nx = {i}\ny = {i * 2}\nprint(x + y)",
            "options": [
                f"Output: {i * 3}",
                f"Output: {i * 2}",
                f"SyntaxError",
                f"TypeError"
            ],
            "correct": 0,
            "explanation": f"In Python, x = {i} and y = {i*2}. Adding x + y results in {i + i*2} = {i*3}."
        })
    return questions

# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION DASHBOARD
# -----------------------------------------------------------------------------
def render_main_app():
    # --- SIDEBAR NAVIGATION & SETTINGS ---
    with st.sidebar:
        st.title("📌 Navigation")
        st.write(f"Logged in as: **{st.session_state.user_email}**")
        
        page = st.radio("Go to:", [
            "🚀 AI Code Reviewer", 
            "📚 Learning Hub", 
            "🎯 100-Question Assessment", 
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        
        # Desktop / Layout Toggle
        desktop = st.checkbox("🖥️ Desktop Mode (Max Width)", value=st.session_state.desktop_mode)
        if desktop != st.session_state.desktop_mode:
            st.session_state.desktop_mode = desktop
            st.rerun()
            
        st.markdown("---")
        
        # Sign Out Option at Bottom
        if st.button("🔴 Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_email = ""
            st.rerun()

    # -------------------------------------------------------------------------
    # PAGE 1: AI CODE REVIEWER
    # -------------------------------------------------------------------------
    if page == "🚀 AI Code Reviewer":
        st.title("🚀 AI Python Code Reviewer")
        st.caption("Paste your Python code below to get instant syntax checks and AI-powered reviews.")
        
        user_code = st.text_area("Write or paste Python code here:", height=250, value="""def calculate_total(items):\n    total = 0\n    for item in items:\n        total += item\n    return total\n\nscores = [85, 90, 78]\nprint("Total:", calculate_total(scores))""")
        
        col_run, col_clear = st.columns([1, 5])
        with col_run:
            run_review = st.button("⚡ Review Code", type="primary")
            
        if run_review:
            if not user_code.strip():
                st.warning("Please enter some Python code to review.")
            else:
                st.markdown("### 🔍 1. AST Syntax Check")
                try:
                    ast.parse(user_code)
                    st.success("✅ AST Syntax Check Passed: No syntax errors detected.")
                except SyntaxError as e:
                    st.error(f"❌ Syntax Error Detected on line {e.lineno}: {e.msg}")
                
                st.markdown("### 🤖 2. Gemini AI Deep Analysis")
                with st.spinner("Analyzing code quality, performance, and security..."):
                    try:
                        # Fetch API key from Streamlit Secrets
                        api_key = st.secrets["GEMINI_API_KEY"]
                        client = genai.Client(api_key=api_key)
                        
                        prompt = f"""
                        You are a Principal Software Engineer. Review the following Python code for:
                        1. Potential logic bugs or edge cases.
                        2. Performance optimizations and Pythonic best practices.
                        3. Security vulnerabilities.
                        4. Refactored / Improved version of the code.

                        Python Code:
                        ```python
                        {user_code}
                        ```
                        """
                        
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        
                        review_result = response.text
                        st.markdown(review_result)
                        
                        # Save to history cache
                        st.session_state.history.append({
                            "code": user_code,
                            "review": review_result
                        })
                        
                    except Exception as err:
                        st.error(f"Error communicating with Gemini API: {err}")

    # -------------------------------------------------------------------------
    # PAGE 2: LEARNING HUB
    # -------------------------------------------------------------------------
    elif page == "📚 Learning Hub":
        st.title("📚 Python Learning Hub")
        st.write("Explore full Python topics with detailed explanations, code examples, and notes.")
        
        topic = st.selectbox("Select Learning Module:", [
            "1. Python Basics & Syntax",
            "2. Data Structures (Lists, Dicts, Sets)",
            "3. Control Flow & Loops",
            "4. Functions & Lambdas",
            "5. Object-Oriented Programming (OOP)",
            "6. Error Handling & Exceptions"
        ])
        
        if topic == "1. Python Basics & Syntax":
            st.markdown("### 🔹 Python Basics & Variables")
            st.write("Python is a high-level, interpreted programming language known for readbility.")
            st.code("""
# Variables and Data Types
name = "Alice"       # String
age = 25            # Integer
gpa = 3.8           # Float
is_student = True   # Boolean

print(f"{name} is {age} years old with GPA {gpa}")
            """, language="python")
            st.info("💡 **Note:** Python uses dynamic typing, meaning you don't need to declare variable types explicitly.")

        elif topic == "2. Data Structures (Lists, Dicts, Sets)":
            st.markdown("### 🔹 Data Structures")
            st.write("Python provides built-in collections to store multiple values.")
            st.code("""
# Lists (Ordered, Mutable)
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")

# Dictionary (Key-Value Pairs)
user = {"name": "Somaiya", "role": "Developer"}

# Set (Unique Values)
unique_numbers = {1, 2, 3, 3, 4} # {1, 2, 3, 4}
            """, language="python")

        elif topic == "5. Object-Oriented Programming (OOP)":
            st.markdown("### 🔹 Object-Oriented Programming")
            st.code("""
class Student:
    def __init__(self, name, major):
        self.name = name
        self.major = major

    def get_details(self):
        return f"Student: {self.name}, Major: {self.major}"

s1 = Student("Alex", "Artificial Intelligence")
print(s1.get_details())
            """, language="python")

    # -------------------------------------------------------------------------
    # PAGE 3: 100-QUESTION ASSESSMENT
    # -------------------------------------------------------------------------
    elif page == "🎯 100-Question Assessment":
        st.title("🎯 Python Skill Test (100 Questions)")
        questions = get_100_quiz_questions()
        
        curr_idx = st.session_state.quiz_index
        q = questions[curr_idx]
        
        # Progress bar
        st.progress((curr_idx + 1) / 100)
        st.caption(f"Question {curr_idx + 1} of 100 | Score: **{st.session_state.quiz_score}** points")
        
        st.markdown(f"### Question {q['id']}: {q['topic']}")
        st.write(q['question'])
        
        if q['code']:
            st.code(q['code'], language="python")
            
        selected_option = st.radio(
            "Select your answer:",
            q['options'],
            key=f"q_{curr_idx}"
        )
        
        col_prev, col_sub, col_next = st.columns([1, 1, 1])
        
        with col_prev:
            if st.button("⬅️ Previous") and curr_idx > 0:
                st.session_state.quiz_index -= 1
                st.rerun()
                
        with col_sub:
            if st.button("✅ Submit Answer"):
                choice_idx = q['options'].index(selected_option)
                if choice_idx == q['correct']:
                    st.success("🎉 Correct!")
                    st.session_state.quiz_score += 10
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
                    
        with col_next:
            if st.button("Next ➡️") and curr_idx < 99:
                st.session_state.quiz_index += 1
                st.rerun()

    # -------------------------------------------------------------------------
    # PAGE 4: SETTINGS & CACHE MANAGEMENT
    # -------------------------------------------------------------------------
    elif page == "⚙️ Settings":
        st.title("⚙️ App Settings & Cache Management")
        
        st.markdown("### 🎨 Appearance & Theme")
        selected_theme = st.radio("Choose Theme:", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🧹 History & Cache Controls")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("🗑️ Clear Review History"):
                st.session_state.history = []
                st.success("Code review history cleared!")
                
        with col_c