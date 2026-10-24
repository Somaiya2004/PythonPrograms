import os
import sys
import ast
from google import genai
from google.genai import errors

def validate_syntax(file_path):
    """Performs a static syntax check using Python's built-in AST module."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        ast.parse(source_code)
        return True, source_code, None
    except SyntaxError as e:
        return False, None, f"Syntax Error at line {e.lineno}, column {e.offset}: {e.text}\nMessage: {e.msg}"
    except Exception as e:
        return False, None, f"Error reading file: {str(e)}"

def review_code_with_ai(source_code, file_path):
    """Sends source code to Gemini for deep bug explanation, security audit, and optimization."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert Principal Python Software Engineer and Code Reviewer. 
    Review the following Python code from file: `{file_path}`.

    Provide your review structured clearly with the following sections using Markdown:
    1. **Summary & Overall Health Score** (Out of 10)
    2. **Bugs, Logic Flaws & Vulnerabilities** (Detailed breakdown of any errors, security risks, or edge cases with explanations)
    3. **Performance & Best Practices** (Suggestions for Pythonic improvements, PEP 8 compliance, and speed optimization)
    4. **Refactored Code** (Provide clean, corrected, and production-ready code block)

    Here is the source code to review:
    ```python
    {source_code}
    ```
    """

    print(f"Analyzing `{file_path}` with Gemini...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except errors.APIError as e:
        return f"API Error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python code_reviewer.py <path_to_python_file.py>")
        sys.exit(1)

    target_file = sys.argv[1]

    if not os.path.exists(target_file):
        print(f"❌ Error: File '{target_file}' not found.")
        sys.exit(1)

    # Step 1: Static AST Validation
    is_valid, source_code, error_msg = validate_syntax(target_file)
    
    if not is_valid:
        print("❌ Static Analysis Failed (Syntax Error Detected):")
        print(error_msg)
        print("\nSending error details to AI for explanation...")
        # Still send to AI so it can explain the syntax error
        with open(target_file, 'r', encoding='utf-8') as f:
            source_code = f.read()

    # Step 2: AI Deep Review & Bug Explanation
    review_report = review_code_with_ai(source_code, target_file)

    # Step 3: Output the Results
    print("\n" + "="*50)
    print(" 🤖 AUTOMATED PYTHON CODE REVIEW REPORT ")
    print("="*50 + "\n")
    print(review_report)

if __name__ == "__main__":
    main()