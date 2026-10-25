import os
import ast
import streamlit as st
from google import genai
from google.genai import errors

# Page Configuration
st.set_page_config(
    page_title="AI Python Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Automated Python Code Reviewer & Bug Explainer")
st.markdown("Paste your Python code below or upload a file to get an instant AI-powered code review, bug analysis, and optimization report.")

# Sidebar for Settings & Secrets
with st.sidebar:
    st.header("Configuration")
    # Automatically pull key from Streamlit Secrets or environment variables
    api_key_input = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    
    st.success("🔒 API Key loaded securely from Secrets.")
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("- Checks for syntax errors instantly using AST.")
    st.markdown("- Powered by **Gemini** for deep logic and security review.")

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
        # Determine API key
        api_key = api_key_input or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            st.error("❌ Error: Gemini API Key is missing. Please enter it in the sidebar or set it in your environment.")
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

                # 2. AI Review via Gemini
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are an expert Principal Python Software Engineer and Code Reviewer. 
                    Review the following Python code snippet.

                    Provide your review structured clearly with the following sections using Markdown:
                    1. **Summary & Overall Health Score** (Out of 10)
                    2. **Bugs, Logic Flaws & Vulnerabilities** (Detailed breakdown of any errors, security risks, or edge cases)
                    3. **Performance & Best Practices** (Suggestions for Pythonic improvements, PEP 8 compliance, and speed optimization)
                    4. **Refactored Code** (Provide clean, corrected, and production-ready code block)

                    Here is the source code to review:
                    ```python
                    {source_code}
                    ```
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    review_result = response.text
                    
                except errors.APIError as e:
                    if getattr(e, 'code', None) == 503:
                        review_result = "⚠️ **Server Busy (503):** The AI model is currently experiencing high demand. Please wait a few seconds and click 'Review Code' again."
                    else:
                        review_result = f"API Error occurred: {e}"
                except Exception as e:
                    review_result = f"An unexpected error occurred: {e}"

            # Display Results
            st.markdown("---")
            
            if not syntax_valid:
                st.error("❌ Static Analysis Warning: Syntax Error detected in your code!")
                st.code(syntax_error_msg, language="text")
            else:
                st.success("✅ Static Analysis Passed: No syntax errors found.")

            st.markdown("### 📋 AI Code Review Report")
            st.markdown(review_result)