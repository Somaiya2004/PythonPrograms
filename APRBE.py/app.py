import os
import ast
import datetime
import streamlit as st
from google import genai
from google.genai import errors, types

# Page Configuration
st.set_page_config(
    page_title="AI Python Studio",
    page_icon="🐍",
    layout="wide"
)

# Initialize Session State for Authentication and History
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "review_history" not in st.session_state:
    st.session_state.review_history = []

# ==========================================
# 1. GOOGLE SIGN-IN GATEWAY
# ==========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("🐍 Welcome to AI Python Studio")
        st.markdown("Sign in with your Google account to access the AI Code Reviewer, History tracker, and Free Python Learning Hub.")
        
        with st.form("login_form"):
            email_input = st.text_input("📧 Google Account Email", placeholder="your.email@gmail.com")
            name_input = st.text_input("👤 Your Full Name", placeholder="Somaiya Shamim")
            submit_login = st.form_submit_button("🔵 Continue with Google", type="primary")
            
            if submit_login:
                if email_input and "@" in email_input:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_input
                    st.session_state.user_name = name_input or "Developer"
                    st.rerun()
                else:
                    st.error("⚠️ Please enter a valid Google email address.")
    st.stop() # Stop execution here until logged in

# ==========================================
# 2. MAIN APP (AFTER SUCCESSFUL LOGIN)
# ==========================================

# Sidebar Navigation & User Info
with st.sidebar:
    st.write(f"👤 **Signed in as:**\n`{st.session_state.user_email}`")
    if st.button("🚪 Sign Out"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.markdown("---")
    st.header("📌 Navigation")
    app_mode = st.radio("Go to:", ["🤖 AI Code Reviewer", "📚 Python Learning Hub", "📜 Review History"])
    
    st.markdown("---")
    # API Key from secrets
    api_key_input = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

# ------------------------------------------
# TAB 1: AI CODE REVIEWER
# ------------------------------------------
if app_mode == "🤖 AI Code Reviewer":
    st.title("🤖 Automated Python Code Reviewer & Bug Explainer")
    st.markdown("Paste your Python code below or upload a file to get an instant AI-powered code review and optimization report.")

    input_method = st.radio("Choose input method:", ["Paste Code", "Upload Python File"], horizontal=True)
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
                st.error("❌ Error: Gemini API Key is missing in secrets.")
            else:
                with st.spinner("Analyzing code structure and generating fast AI review..."):
                    # 1. AST Syntax Check
                    syntax_valid = True
                    syntax_error_msg = None
                    try:
                        ast.parse(source_code)
                    except SyntaxError as e:
                        syntax_valid = False
                        syntax_error_msg = f"Syntax Error at line {e.lineno}: {e.msg}"
                    except Exception as e:
                        syntax_valid = False
                        syntax_error_msg = str(e)

                    # 2. Gemini Fast Review
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = f"""
                        You are an expert Principal Python Software Engineer. Review the following Python code concisely:
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
                        
                        # Save to History
                        st.session_state.review_history.insert(0, {
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "code": source_code[:100] + "..." if len(source_code) > 100 else source_code,
                            "report": review_result
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
                    st.error(f"❌ Static Analysis Warning: {syntax_error_msg}")
                else:
                    st.success("✅ Static Analysis Passed: No syntax errors found.")

                st.markdown("### 📋 AI Code Review Report")
                st.markdown(review_result)

# ------------------------------------------
# TAB 2: PYTHON LEARNING HUB
# ------------------------------------------
elif app_mode == "📚 Python Learning Hub":
    st.title("📚 Free Python Learning Sessions")
    st.markdown("Master Python programming from scratch with our quick, structured interactive modules!")

    lesson = st.selectbox("Choose a Learning Module:", [
        "1. Variables & Data Types",
        "2. Control Flow (If/Else & Loops)",
        "3. Functions & Scope",
        "4. Error Handling (Try/Except)",
        "5. Object-Oriented Programming (Classes)"
    ])

    st.markdown("---")

    if "1." in lesson:
        st.subheader("Session 1: Variables & Data Types")
        st.markdown("Variables are containers for storing data values. Python has no command for declaring a variable.")
        st.code("""
# Example code
x = 5           # integer
name = "Python" # string
price = 19.99   # float
is_active = True # boolean

print(type(x))
        """, language="python")
        st.info("💡 **Practice Tip:** Try pasting this into the Code Reviewer tab to check its quality!")

    elif "2." in lesson:
        st.subheader("Session 2: Control Flow (If/Else & Loops)")
        st.markdown("Conditional statements allow your program to make decisions based on conditions.")
        st.code("""
# If-Else Example
age = 18
if age >= 18:
    print("Eligible to vote")
else:
    print("Not eligible")

# For Loop Example
for i in range(3):
    print(f"Iteration {i}")
        """, language="python")

    elif "3." in lesson:
        st.subheader("Session 3: Functions & Scope")
        st.markdown("A function is a block of code which only runs when it is called. Use the `def` keyword.")
        st.code("""
def calculate_area(length, width):
    return length * width

result = calculate_area(10, 5)
print(result) # Output: 50
        """, language="python")

    elif "4." in lesson:
        st.subheader("Session 4: Error Handling")
        st.markdown("The `try` block lets you test a block of code for errors, and `except` handles them.")
        st.code("""
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You cannot divide by zero!")
        """, language="python")

    elif "5." in lesson:
        st.subheader("Session 5: Object-Oriented Programming")
        st.markdown("Python is an object oriented programming language. Almost everything in Python is an object, with its properties and methods.")
        st.code("""
class Dog:
    def __init__(self, name):
        self.name = name
        
    def bark(self):
        return f"{self.name} says Woof!"

my_dog = Dog("Buddy")
print(my_dog.bark())
        """, language="python")

# ------------------------------------------
# TAB 3: REVIEW HISTORY
# ------------------------------------------
elif app_mode == "📜 Review History":
    st.title("📜 Past Code Reviews")
    st.markdown("Here is the history of code reviews performed during your current session.")

    if not st.session_state.review_history:
        st.info("ℹ️ No review history yet. Go to the **AI Code Reviewer** tab and review a snippet!")
    else:
        for idx, item in enumerate(st.session_state.review_history):
            with st.expander(f"Review #{len(st.session_state.review_history) - idx} — {item['time']}"):
                st.markdown(f"**Snippet Preview:**")
                st.code(item['code'], language="python")
                st.markdown(f"**Full Report:**")
                st.markdown(item['report'])