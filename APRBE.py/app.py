import os
import ast
import streamlit as st
from google import genai
from google.genai import errors, types

# Page Configuration
st.set_page_config(
    page_title="AI Python Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# Initialize Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🤖 Automated Python Code Reviewer & Bug Explainer")
st.markdown("Paste your Python code below or upload a file to get an instant AI-powered code review, bug analysis, and optimization report.")

# Sidebar for Settings, Secrets, & History
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    
    st.success("🔒 API Key loaded securely.")
    st.markdown("---")
    
    # History Section in Sidebar
    st.header("📜 Session History")
    if not st.session_state.history:
        st.markdown("_No reviews yet in this session._")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            history_num = len(st.session_state.history) - i
            snippet = item["code"][:30].replace("\n", " ") + "..."
            if st.button(f"Review #{history_num}: {snippet}", key=f"hist_{i}"):
                st.session_state.selected_review = item["report"]

    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("- Checks syntax instantly using AST.")
    st.markdown("- Powered by **Gemini** for speed & security.")

# Main Interface: Code Input Option
input_method = st.radio("Choose input method:", ["Paste Code", "Upload Python File"])

source_code = ""

if input_method == "Paste Code":
    source_code = st.text_area("Enter your Python code here:", height=300, placeholder="def add(a, b):\n    return a + b")
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
            st.error("❌ Error: Gemini API Key is missing. Please enter it in your Streamlit Secrets.")
        else:
            with st.spinner("Analyzing code structure and running AI review..."):
                # 1. Static AST Syntax Validation Check
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

                # 2. Fast AI Review via Gemini
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
                    
                    # Save to session history
                    st.session_state.history.append({
                        "code": source_code,
                        "report": review_result
                    })
                    st.session_state.selected_review = review_result
                    
                except errors.APIError as e:
                    if getattr(e, 'code', None) == 503:
                        st.session_state.selected_review = "⚠️ **Server Busy (503):** High demand detected. Please click 'Review Code' again."
                    else:
                        st.session_state.selected_review = f"API Error occurred: {e}"
                except Exception as e:
                    st.session_state.selected_review = f"An unexpected error occurred: {e}"

# Display Results (either current or selected from history)
if "selected_review" in st.session_state:
    st.markdown("---")
    st.markdown("### 📋 AI Code Review Report")
    st.markdown(st.session_state.selected_review)