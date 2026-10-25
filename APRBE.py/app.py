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
if "review_history" not in st.session_state:
    st.session_state.review_history = []

# ==========================================
# 1. GOOGLE SIGN-IN GATE
# ==========================================
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🔐 Welcome to Python Hub")
        st.markdown("Please sign in with your Google account to access the AI Code Reviewer and Free Python Learning Academy.")
        
        with st.form("login_form"):
            google_email = st.text_input("Google Email Address", placeholder="your.name@gmail.com")
            submit_login = st.form_submit_button("Sign in with Google 🚀", use_container_width=True)
            
            if submit_login:
                if google_email and "@" in google_email:
                    st.session_state.authenticated = True
                    st.session_state.user_email = google_email
                    st.rerun()
                else:
                    st.error("⚠️ Please enter a valid Google email address.")
    
    st.stop()  # Stop execution here until logged in

# ==========================================
# 2. MAIN APP (AFTER AUTHENTICATION)
# ==========================================

# Sidebar Profile & Navigation
with st.sidebar:
    st.header("👤 Account")
    st.success(f"Signed in as:\n**{st.session_state.user_email}**")
    if st.button("🚪 Sign Out"):
        st.session_state.authenticated = False
        st.session_state.user_email = ""
        st.rerun()
        
    st.markdown("---")
    st.header("⚙️ Configuration")
    api_key_input = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    st.success("🔒 API Key loaded securely.")
    
    st.markdown("---")
    st.markdown("### 💡 Hub Features")
    st.markdown("- Instant AI Code Review")
    st.markdown("- Free Python Notes & Tutorials")
    st.markdown("- Session Review History")

st.title("🐍 Python Hub: AI Reviewer & Learning Academy")
st.markdown("Your all-in-one platform to review Python code, check bugs instantly, and learn Python from scratch for free.")

# Main Navigation Tabs
tab_reviewer, tab_learning, tab_history = st.tabs(["🤖 AI Code Reviewer", "📚 Python Learning Hub", "📜 Review History"])

# --- TAB 1: AI CODE REVIEWER ---
with tab_reviewer:
    input_method = st.radio("Choose input method:", ["Paste Code", "Upload Python File"], key="input_method_radio")

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
            api_key = api_key_input or os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                st.error("❌ Error: Gemini API Key is missing.")
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
                        
                        config = types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=1500,
                        )
                        
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=prompt,
                            config=config,
                        )
                        review_result = response.text
                        
                        # Save to history session state
                        st.session_state.review_history.insert(0, {
                            "code": source_code[:100] + "..." if len(source_code) > 100 else source_code,
                            "result": review_result
                        })
                        
                    except errors.APIError as e:
                        if getattr(e, 'code', None) == 503:
                            review_result = "⚠️ **Server Busy (503):** High demand detected. Please click 'Review Code' again."
                        else:
                            review_result = f"API Error occurred: {e}"
                    except Exception as e:
                        review_result = f"An unexpected error occurred: {e}"

                st.markdown("---")
                if not syntax_valid:
                    st.error("❌ Static Analysis Warning: Syntax Error detected in your code!")
                    st.code(syntax_error_msg, language="text")
                else:
                    st.success("✅ Static Analysis Passed: No syntax errors found.")

                st.markdown("### 📋 AI Code Review Report")
                st.markdown(review_result)

# --- TAB 2: PYTHON LEARNING HUB ---
with tab_learning:
    st.header("📚 Free Python Learning Sessions & Notes")
    st.markdown("Master Python from scratch with curated notes, code examples, and practice exercises.")
    
    topic = st.selectbox("Select a Learning Module:", [
        "1. Python Basics & Variables",
        "2. Control Flow (If-Else & Loops)",
        "3. Functions & Scope",
        "4. Data Structures (Lists, Dictionaries, Sets)",
        "5. Object-Oriented Programming (OOP)"
    ])
    
    st.markdown("---")
    
    if "Basics" in topic:
        st.subheader("Module 1: Python Basics & Variables")
        st.markdown("""
        Python is a high-level, interpreted programming language known for its readability.
        
        * **Variables:** Containers for storing data values. Unlike other languages, Python has no command for declaring a variable.
        ```python
        x = 5
        name = "Somaiya"
        print(x, name)
        ```
        * **Data Types:** `int` (integers), `float` (decimals), `str` (strings), `bool` (booleans).
        """)
    elif "Control Flow" in topic:
        st.subheader("Module 2: Control Flow")
        st.markdown("""
        Control flow allows your program to make decisions and repeat tasks.
        
        * **Conditionals:** `if`, `elif`, `else`
        ```python
        age = 20
        if age >= 18:
            print("Eligible to vote")
        else:
            print("Minor")
        ```
        * **Loops:** `for` loops iterate over sequences, while `while` loops run as long as a condition is true.
        """)
    elif "Functions" in topic:
        st.subheader("Module 3: Functions & Scope")
        st.markdown("""
        Functions are blocks of reusable code designed to perform a specific task.
        
        ```python
        def calculate_area(length, width):
            return length * width

        result = calculate_area(10, 5)
        print(result) # Output: 50
        ```
        """)
    elif "Data Structures" in topic:
        st.subheader("Module 4: Data Structures")
        st.markdown("""
        * **Lists:** Ordered, mutable collections `[1, 2, 3]`
        * **Dictionaries:** Key-value pairs `{"name": "Alice", "age": 25}`
        * **Sets:** Unordered collections with unique elements `{1, 2, 3}`
        """)
    else:
        st.subheader("Module 5: Object-Oriented Programming (OOP)")
        st.markdown("""
        OOP is a programming paradigm using classes and objects.
        
        ```python
        class Car:
            def __init__(self, brand):
                self.brand = brand

            def horn(self):
                return f"{self.brand} goes beep beep!"

my_car = Car("Toyota")
print(my_car.horn())
        ```
        """)

# --- TAB 3: REVIEW HISTORY ---
with tab_history:
    st.header("📜 Past Code Reviews")
    if not st.session_state.review_history:
        st.info("No reviews recorded yet in this session. Run a code review in the first tab to see your history here!")
    else:
        for i, item in enumerate(st.session_state.review_history):
            with st.expander(f"Review #{len(st.session_state.review_history) - i}: {item['code']} ..."):
                st.markdown(item['result'])