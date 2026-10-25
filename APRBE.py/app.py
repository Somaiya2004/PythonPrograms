import os
import ast
import streamlit as st
from google import genai
from google.genai import errors, types

# Page Configuration
st.set_page_config(
    page_title="Python Hub: AI Reviewer & Academy",
    page_icon="🐍",
    layout="wide"
)

# Initialize Session States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "review_history" not in st.session_state:
    st.session_state.review_history = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# ==========================================
# 1. GOOGLE SIGN-IN GATE (OPENING PAGE)
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔵 Google Sign-In</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Sign in with your Google account to access Python Hub</p>", unsafe_allow_html=True)
        
        with st.form("google_login_form"):
            email = st.text_input("Email or phone", placeholder="your.name@gmail.com")
            password = st.text_input("Google Account Password", type="password", placeholder="••••••••••••")
            
            submit_login = st.form_submit_button("Sign In 🚀", use_container_width=True)
            
            if submit_login:
                if email and "@" in email and len(password) >= 6:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.success("Login successful! Loading Python Hub...")
                    st.rerun()
                else:
                    st.error("⚠️ Please enter a valid Google email and a password (at least 6 characters).")
    
    st.stop()  # Stop execution here until authenticated

# ==========================================
# 2. SIDEBAR & NAVIGATION (INSIDE APP)
# ==========================================
with st.sidebar:
    st.markdown("### 👤 Google Account")
    st.info(f"**{st.session_state.user_email}**\n\n🏆 Score: **{st.session_state.score} XP**")
    
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    navigation = st.radio("Go to:", [
        "🖥️ Desktop", 
        "🤖 AI Code Reviewer", 
        "📚 Learning Hub (Notes)", 
        "📝 Test Your Ability (Quiz)", 
        "⚙️ Settings"
    ])
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sign Out Button at the bottom
    if st.button("🚪 Sign Out", use_container_width=True, type="secondary"):
        st.session_state.authenticated = False
        st.session_state.user_email = ""
        st.rerun()

# ==========================================
# 3. APP VIEWS BASED ON NAVIGATION
# ==========================================

# --- DESKTOP VIEW ---
if navigation == "🖥️ Desktop":
    st.title("🖥️ Python Hub Desktop")
    st.markdown(f"Welcome back, **{st.session_state.user_email}**! Here is your command center.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Your Current Score", value=f"{st.session_state.score} XP")
    with col2:
        st.metric(label="Reviews Performed", value=len(st.session_state.review_history))
    with col3:
        st.metric(label="Status", value="Active 🟢")
        
    st.markdown("---")
    st.markdown("### 🚀 Quick Access")
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **AI Code Reviewer:** Paste your code and let Gemini inspect bugs, security flaws, and refactor it instantly.")
    with c2:
        st.info("📚 **Learning Hub:** Access complete Python notes, master coding concepts, and take ability tests to gain score points!")

# --- AI CODE REVIEWER VIEW ---
elif navigation == "🤖 AI Code Reviewer":
    st.title("🤖 AI Code Reviewer & Bug Explainer")
    st.markdown("Paste your Python code or upload a file for an instant AI-powered engineering review.")
    
    input_method = st.radio("Choose input method:", ["Paste Code", "Upload Python File"], key="code_input_method")
    source_code = ""
    
    if input_method == "Paste Code":
        source_code = st.text_area("Enter your Python code here:", height=250, placeholder="def add(a, b):\n    return a + b")
    else:
        uploaded_file = st.file_uploader("Upload a .py file", type=["py"])
        if uploaded_file is not None:
            try:
                source_code = uploaded_file.read().decode("utf-8")
                st.code(source_code, language="python")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    if st.button("🚀 Review Code", type="primary"):
        if not source_code.strip():
            st.warning("⚠️ Please provide some Python code to review.")
        else:
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                st.error("❌ Error: Gemini API Key is missing in secrets.")
            else:
                with st.spinner("Analyzing code structure and running AI review..."):
                    # AST Check
                    syntax_error_msg = None
                    try:
                        ast.parse(source_code)
                        syntax_valid = True
                    except SyntaxError as e:
                        syntax_valid = False
                        syntax_error_msg = f"Syntax Error at line {e.lineno}, column {e.offset}: {e.text}\nMessage: {e.msg}"
                    except Exception as e:
                        syntax_valid = False
                        syntax_error_msg = str(e)

                    # Gemini Review
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = f"""
                        You are an expert Principal Python Software Engineer. Review the following Python code snippet concisely:
                        1. **Summary & Health Score** (Out of 10)
                        2. **Bugs & Vulnerabilities**
                        3. **Performance & Best Practices**
                        4. **Refactored Code**

                        Code to review:
                        ```python
                        {source_code}
                        ```
                        """
                        config = types.GenerateContentConfig(temperature=0.2, max_output_tokens=1500)
                        response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt, config=config)
                        review_result = response.text
                        
                        # Save history
                        st.session_state.review_history.insert(0, {"code": source_code[:80], "result": review_result})
                        
                    except errors.APIError as e:
                        err_code = getattr(e, 'code', None)
                        if err_code == 503:
                            review_result = "⚠️ **Server Busy (503):** High demand detected. Please click 'Review Code' again."
                        elif err_code == 429:
                            review_result = "⚠️ **Quota Exceeded (429):** Free daily limit reached. Please check your API key."
                        else:
                            review_result = f"API Error: {e}"
                    except Exception as e:
                        review_result = f"Error: {e}"

                st.markdown("---")
                if not syntax_valid:
                    st.error("❌ Static Analysis Warning: Syntax Error detected!")
                    st.code(syntax_error_msg, language="text")
                else:
                    st.success("✅ Static Analysis Passed: No syntax errors found.")

                st.markdown("### 📋 AI Code Review Report")
                st.markdown(review_result)

# --- LEARNING HUB VIEW (NOTES) ---
elif navigation == "📚 Learning Hub (Notes)":
    st.title("📚 Python Learning Hub & Free Notes")
    st.markdown("Explore comprehensive study notes ranging from beginner basics to advanced Object-Oriented Programming.")
    
    module = st.selectbox("Select Learning Module:", [
        "1. Python Syntax & Variables",
        "2. Control Flow (If-Else & Loops)",
        "3. Functions & Lambda Expressions",
        "4. Data Structures (Lists, Dictionaries, Sets)",
        "5. Object-Oriented Programming (OOP)"
    ])
    
    st.markdown("---")
    
    if "Syntax" in module:
        st.subheader("Module 1: Python Syntax & Variables")
        st.markdown("""
        Python relies on indentation for block scoping rather than curly braces.
        * **Variables:** Containers for storing data values.
        ```python
        name = "Somaiya"
        score = 95
        is_active = True
        ```
        * **Type Casting:** Converting variables from one type to another (`int()`, `str()`, `float()`).
        """)
    elif "Control Flow" in module:
        st.subheader("Module 2: Control Flow")
        st.markdown("""
        * **Conditional Statements:**
        ```python
        marks = 85
        if marks >= 90:
            print("Grade A")
        elif marks >= 75:
            print("Grade B")
        else:
            print("Grade C")
        ```
        * **Loops:** `for item in sequence:` and `while condition:`
        """)
    elif "Functions" in module:
        st.subheader("Module 3: Functions & Lambda")
        st.markdown("""
        * **Defining Functions:**
        ```python
        def greet(user):
            return f"Hello, {user}!"
        ```
        * **Lambda Functions:** Anonymous inline functions: `square = lambda x: x * x`
        """)
    elif "Data Structures" in module:
        st.subheader("Module 4: Data Structures")
        st.markdown("""
        * **Lists:** Ordered and mutable `my_list = [1, 2, "apple"]`
        * **Dictionaries:** Key-value mappings `student = {"name": "Alex", "age": 22}`
        * **Sets:** Unordered collections of unique items `{1, 2, 3}`
        """)
    else:
        st.subheader("Module 5: Object-Oriented Programming (OOP)")
        st.markdown("""
        * **Classes and Objects:**
        ```python
        class Dog:
            def __init__(self, name):
                self.name = name
            def bark(self):
                return f"{self.name} says Woof!"

        my_dog = Dog("Buddy")
        print(my_dog.bark())
        ```
        """)

# --- TEST YOUR ABILITY VIEW (QUIZ & SCORE) ---
elif navigation == "📝 Test Your Ability (Quiz)":
    st.title("📝 Test Your Python Ability")
    st.markdown("Answer the coding questions below to test your skills and **gain XP score points**!")
    
    with st.form("quiz_form"):
        st.markdown("#### Q1: What is the correct file extension for Python files?")
        q1 = st.radio("Choose one:", [".pt", ".py", ".python", ".pyt"], key="q1")
        
        st.markdown("#### Q2: Which keyword is used to define a function in Python?")
        q2 = st.radio("Choose one:", ["function", "def", "fun", "define"], key="q2")
        
        st.markdown("#### Q3: What data type is the result of expression `10 == 10`?")
        q3 = st.radio("Choose one:", ["int", "float", "bool", "str"], key="q3")
        
        submit_quiz = st.form_submit_button("Submit Answers 🎯", use_container_width=True)
        
        if submit_quiz:
            earned_points = 0
            if q1 == ".py":
                earned_points += 10
            if q2 == "def":
                earned_points += 10
            if q3 == "bool":
                earned_points += 10
                
            st.session_state.score += earned_points
            st.success(f"🎉 Quiz submitted! You earned **+{earned_points} XP**. Total Score: **{st.session_state.score} XP**")

# --- SETTINGS VIEW ---
elif navigation == "⚙️ Settings":
    st.title("⚙️ Account & API Settings")
    st.markdown(f"**Signed in user:** `{st.session_state.user_email}`")
    st.markdown(f"**Total Score:** `{st.session_state.score} XP`")
    
    st.markdown("---")
    st.subheader("🔑 Gemini API Key Configuration")
    custom_key = st.text_input("Override Gemini API Key (Optional):", type="password", placeholder="AIzaSy...")
    if custom_key:
        os.environ["GEMINI_API_KEY"] = custom_key
        st.success("Custom API key applied successfully!")
    
    st.markdown("---")
    st.markdown("### 📜 Session History")
    if not st.session_state.review_history:
        st.info("No past code reviews recorded yet.")
    else:
        for i, item in enumerate(st.session_state.review_history):
            with st.expander(f"Review #{len(st.session_state.review_history) - i}: {item['code']}..."):
                st.markdown(item['result'])