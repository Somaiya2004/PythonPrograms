import streamlit as st
import ast
import zipfile
import io
import requests
import json

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME CUSTOMIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PyReview AI - Automated Python Review & Bug Explainer",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "profile_completed" not in st.session_state:
    st.session_state.profile_completed = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "first_name" not in st.session_state:
    st.session_state.first_name = ""
if "last_name" not in st.session_state:
    st.session_state.last_name = ""
if "profession" not in st.session_state:
    st.session_state.profession = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "history" not in st.session_state:
    st.session_state.history = []
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "coding_solved" not in st.session_state:
    st.session_state.coding_solved = []

# Theme Colors
if st.session_state.theme == "Dark":
    bg_color = "#0e1117"
    card_bg = "#1e222a"
    text_color = "#ffffff"
else:
    bg_color = "#f8f9fa"
    card_bg = "#ffffff"
    text_color = "#212529"

st.markdown(f"""
    <style>
    .main {{ background-color: {bg_color}; color: {text_color}; }}
    .stApp {{ background-color: {bg_color}; }}
    .app-card {{
        background-color: {card_bg};
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }}
    .logo-header {{
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. AUTHENTICATION & PROFILE SETUP FLOWS
# -----------------------------------------------------------------------------
def render_auth():
    st.markdown("<div style='text-align: center; margin-top: 40px;'>", unsafe_allow_html=True)
    st.markdown("<span class='logo-header'>🐍 PyReview AI</span>", unsafe_allow_html=True)
    st.markdown("### Automated Python Code Reviewer & Bug Explainer", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
        
        with tab1:
            email = st.text_input("Email / Username", key="signin_user")
            password = st.text_input("Password", type="password", key="signin_pass")
            if st.button("🚀 Login", use_container_width=True):
                if email and password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Please fill in your credentials.")
            
            st.markdown("---")
            if st.button("🌐 Continue with Google Account", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_email = "google_user@gmail.com"
                st.rerun()

        with tab2:
            new_email = st.text_input("Email Address", key="signup_email")
            new_pass = st.text_input("Create Password", type="password", key="signup_pass")
            if st.button("✨ Register Now", use_container_width=True):
                if new_email and new_pass:
                    st.session_state.authenticated = True
                    st.session_state.user_email = new_email
                    st.rerun()
                else:
                    st.error("Please enter required fields.")
        st.markdown("</div>", unsafe_allow_html=True)

def render_profile_setup():
    st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
    st.markdown("<span class='logo-header'>👤 Complete Your Profile</span>", unsafe_allow_html=True)
    st.markdown("<p>Tell us a bit about yourself to personalize your experience.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        profession = st.selectbox("Profession", ["Student / Learner", "Software Engineer", "Data Scientist", "Python Hobbyist", "Educator"])
        uname = st.text_input("Username")
        
        if st.button("💾 Save & Launch Dashboard", type="primary", use_container_width=True):
            if fname and lname and uname:
                st.session_state.first_name = fname
                st.session_state.last_name = lname
                st.session_state.profession = profession
                st.session_state.username = uname
                st.session_state.profile_completed = True
                st.rerun()
            else:
                st.error("Please fill out all required profile details.")
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. OLLAMA LOCAL AI CALL HELPER
# -----------------------------------------------------------------------------
def query_ollama(prompt):
    """Calls local Ollama instance running a fast model like codellama or llama3."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "codellama",  # Fallback/standard local model name
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        else:
            return f"⚠️ Ollama returned status code {response.status_code}. Make sure Ollama is running locally (`ollama serve`)."
    except Exception as e:
        return f"⚠️ Could not connect to local Ollama server at `http://localhost:11434`. Ensure Ollama is installed and running (`ollama run codellama`). Error: {e}"

# -----------------------------------------------------------------------------
# 4. MAIN APP DASHBOARD WITH 3-DOT MENU & 6 FEATURES
# -----------------------------------------------------------------------------
def render_main_app():
    # Top bar with branding and 3-Dot Quick Menu
    top_col1, top_col2 = st.columns([6, 1])
    with top_col1:
        st.markdown("<span class='logo-header'>🐍 PyReview AI Studio</span>", unsafe_allow_html=True)
    with top_col2:
        # 3-Dot Menu popover
        with st.popover("⋮ ⚙️ Menu"):
            st.write(f"**User:** @{st.session_state.username or 'Developer'}")
            st.write(f"**Email:** {st.session_state.user_email}")
            st.write(f"**Profession:** {st.session_state.profession}")
            st.markdown("---")
            if st.button("👤 View Profile Details"):
                st.info(f"Name: {st.session_state.first_name} {st.session_state.last_name}\nUsername: @{st.session_state.username}")
            
            theme_choice = st.radio("Theme Mode", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
            if theme_choice != st.session_state.theme:
                st.session_state.theme = theme_choice
                st.rerun()
                
            if st.button("🚪 Logout", type="primary", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.profile_completed = False
                st.rerun()

    st.markdown("---")

    # Sidebar Navigation (5-6 features)
    with st.sidebar:
        st.markdown("### 🧭 Navigation Hub")
        feature = st.radio("Select Tool:", [
            "🚀 AI Code Reviewer", 
            "📚 Learning Hub", 
            "🎥 Learning Tutorials", 
            "🎯 Quiz Assessment", 
            "💻 Coding Practice", 
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        st.markdown(f"**Logged in as:**\n@{st.session_state.username or 'User'}")

    # =========================================================================
    # FEATURE 1: AI CODE REVIEWER (Text, .py file, .zip support)
    # =========================================================================
    if feature == "🚀 AI Code Reviewer":
        st.title("🚀 Automated AI Code Reviewer & Bug Explainer")
        st.caption("Powered by local Ollama for lightning-fast, secure, and offline code analysis.")
        
        input_method = st.radio("Choose Input Method:", ["✏️ Paste Code", "📁 Upload Python File (.py)", "📦 Upload Zip Project (.zip)"], horizontal=True)
        
        source_code = ""
        if input_method == "✏️ Paste Code":
            source_code = st.text_area("Paste your Python code here:", height=250, value="def calculate_discount(price, rate):\n    return price - (price * rate)\n\nprint(calculate_discount(100, 0.2))")
            
        elif input_method == "📁 Upload Python File (.py)":
            py_file = st.file_uploader("Upload a `.py` file", type=["py"])
            if py_file is not None:
                source_code = py_file.read().decode("utf-8")
                st.code(source_code, language="python")
                
        elif input_method == "📦 Upload Zip Project (.zip)":
            zip_file = st.file_uploader("Upload a `.zip` file containing Python code", type=["zip"])
            if zip_file is not None:
                with zipfile.ZipFile(io.BytesIO(zip_file.read())) as z:
                    py_files = [f for f in z.namelist() if f.endswith('.py')]
                    if py_files:
                        selected_py = st.selectbox("Select file to review from ZIP:", py_files)
                        with z.open(selected_py) as f:
                            source_code = f.read().decode("utf-8")
                            st.code(source_code, language="python")
                    else:
                        st.warning("No `.py` files found in the uploaded zip archive.")

        if st.button("⚡ Run Fast AI Review & Bug Check", type="primary"):
            if not source_code.strip():
                st.warning("Please provide or upload valid Python code.")
            else:
                st.markdown("### 🔍 1. AST Syntax Validation")
                try:
                    ast.parse(source_code)
                    st.success("✅ AST Check Passed: No syntax errors detected.")
                except SyntaxError as e:
                    st.error(f"❌ Syntax Error on Line {e.lineno}: {e.msg}")

                st.markdown("### 🤖 2. Local Ollama Deep Bug Analysis")
                with st.spinner("Analyzing code quality and debugging with Ollama..."):
                    prompt = f"""
                    You are an expert Python Code Reviewer and Debugger. Analyze this code for bugs, performance issues, and best practices. Give a refactored version.
                    
                    Python Code:
                    ```python
                    {source_code}
                    ```
                    """
                    analysis = query_ollama(prompt)
                    st.markdown(analysis)

    # =========================================================================
    # FEATURE 2: LEARNING HUB (Basic to Advanced with 2+ Code Samples)
    # =========================================================================
    elif feature == "📚 Learning Hub":
        st.title("📚 Comprehensive Python Learning Hub")
        st.write("Explore structured modules from basic to advanced with detailed explanations and sample codes.")
        
        module = st.selectbox("Select Python Topic:", [
            "1. Variables & Data Types",
            "2. Control Flow & Loops",
            "3. Functions & Lambda Expressions",
            "4. Advanced Data Structures (Lists, Dicts, Sets)",
            "5. Object-Oriented Programming (OOP)",
            "6. Error Handling & Custom Exceptions",
            "7. Asynchronous Programming & Concurrency"
        ])
        
        if "1." in module:
            st.subheader("🔹 1. Variables & Data Types")
            st.write("Python handles variable assignments dynamically without explicit type declarations. Below are sample codes demonstrating basic data types.")
            st.code("""
# Sample 1: Basic Types and Type Conversion
name = "Alice"      # String
age = 24            # Integer
price = 99.50       # Float
is_active = True    # Boolean

print(f"User {name}, Age: {age}, Status: {is_active}")
            """, language="python")
            st.code("""
# Sample 2: Mutable vs Immutable References
x = [1, 2, 3] # List is mutable
y = x
y.append(4)
print("x:", x) # Both reflect change
            """, language="python")
            st.info("💡 **Key Note:** Always be careful with mutable default arguments in Python functions.")

        elif "3." in module:
            st.subheader("🔹 3. Functions & Lambda Expressions")
            st.write("Functions encapsulate reusable blocks of logic. Lambda functions provide quick anonymous functions.")
            st.code("""
# Sample 1: Standard function with default arguments
def calculate_tax(amount, rate=0.05):
    return amount * (1 + rate)

print(calculate_tax(200))
            """, language="python")
            st.code("""
# Sample 2: Lambda function with filter & map
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)
            """, language="python")

    # =========================================================================
    # FEATURE 3: LEARNING TUTORIALS (Video / Bug Solving Guides)
    # =========================================================================
    elif feature == "🎥 Learning Tutorials":
        st.title("🎥 Python Bug-Fixing & Mastery Tutorials")
        st.write("Explore curated video walkthroughs and guides from beginner debugging to advanced software architecture.")
        
        tab_b, tab_m, tab_a = st.tabs(["🟢 Beginner Bug Guides", "🟡 Intermediate Debugging", "🔴 Advanced Architecture"])
        
        with tab_b:
            st.markdown("### Beginner Bug Guide #1: Fixing `NameError` and `TypeError`")
            st.write("Learn why variables need initialization before usage and how type mismatches happen in arithmetic operations.")
            st.video("https://www.youtube.com/watch?v=_uQrJ0TkZlc")
            
        with tab_m:
            st.markdown("### Intermediate Guide: Mastering Dictionary Lookups & KeyError handling")
            st.write("Discover the `.get()` method and `defaultdict` to prevent app crashes when keys are missing.")
            
        with tab_a:
            st.markdown("### Advanced Guide: Memory Management and Garbage Collection in Python")
            st.write("Deep dive into reference counting, circular references, and GC modules.")

    # =========================================================================
    # FEATURE 4: QUIZ ASSESSMENT & SCORE TRACKING
    # =========================================================================
    elif feature == "🎯 Quiz Assessment":
        st.title("🎯 Python Skill Assessment Quiz")
        st.write("Test your Python knowledge, track your progress, and check your leaderboard ranking.")
        
        questions = [
            {"q": "What is the output of `type(1/2)` in Python 3?", "options": ["int", "float", "double", "decimal"], "correct": 1},
            {"q": "Which keyword is used to create an anonymous function in Python?", "options": ["def", "function", "lambda", "anon"], "correct": 2},
            {"q": "What does `is` operator check in Python?", "options": ["Value equality", "Memory address equality", "Type equality", "Size equality"], "correct": 1},
        ]
        
        score = st.session_state.quiz_score
        st.metric(label="Your Total XP Score", value=score)
        
        for idx, item in enumerate(questions):
            st.markdown(f"**Q{idx+1}: {item['q']}**")
            ans = st.radio("Choose answer:", item["options"], key=f"quiz_q_{idx}")
            if st.button(f"Submit Q{idx+1}", key=f"sub_{idx}"):
                if item["options"].index(ans) == item["correct"]:
                    st.success("🎉 Correct! +10 XP")
                    st.session_state.quiz_score += 10
                else:
                    st.error("❌ Incorrect. Try again!")
                    
        st.markdown("---")
        st.markdown("### 🏆 Leaderboard Note")
        st.info("Remember: Rank is dynamic and changes as others practice! You don't always have to be #1 to make great progress.")

    # =========================================================================
    # FEATURE 5: CODING PRACTICE (Beginner to Advanced Questions)
    # =========================================================================
    elif feature == "💻 Coding Practice":
        st.title("💻 Hands-On Coding Practice")
        st.write("Solve coding challenges ranging from beginner to advanced level to sharpen your logic.")
        
        level = st.selectbox("Select Difficulty:", ["Beginner", "Intermediate", "Advanced"])
        
        if level == "Beginner":
            st.markdown("### Challenge 1: Check Even or Odd")
            st.write("Write a function `is_even(n)` that returns `True` if `n` is even, otherwise `False`.")
            user_sol = st.text_area("Your Code Solution:", value="def is_even(n):\n    return n % 2 == 0", height=120)
            if st.button("Run Test Cases"):
                try:
                    local_scope = {}
                    exec(user_sol, {}, local_scope)
                    func = local_scope.get("is_even")
                    if func(4) == True and func(5) == False:
                        st.success("✅ All test cases passed! Great job.")
                    else:
                        st.error("❌ Test cases failed. Check your logic.")
                except Exception as e:
                    st.error(f"Execution Error: {e}")
                    
        elif level == "Intermediate":
            st.markdown("### Challenge 2: Palindrome Checker")
            st.write("Write a function `is_palindrome(s)` that returns `True` if string `s` is a palindrome (ignoring spaces/case).")
            
        elif level == "Advanced":
            st.markdown("### Challenge 3: LRU Cache Implementation")
            st.write("Implement a Least Recently Used (LRU) cache with `get(key)` and `put(key, value)` methods in $O(1)$ time.")

    # =========================================================================
    # FEATURE 6: SETTINGS & PREFERENCES
    # =========================================================================
    elif feature == "⚙️ Settings":
        st.title("⚙️ Application Settings")
        st.write(f"Manage your account, preferences, and local cache.")
        
        st.subheader("🎨 Appearance")
        chosen_theme = st.radio("Theme Mode", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
        if chosen_theme != st.session_state.theme:
            st.session_state.theme = chosen_theme
            st.rerun()
            
        st.markdown("---")
        st.subheader("🧹 Data & Cache Management")
        if st.button("🗑️ Clear Review History"):
            st.session_state.history = []
            st.success("Review history wiped successfully.")

# -----------------------------------------------------------------------------
# 5. MAIN ROUTER
# -----------------------------------------------------------------------------
if not st.session_state.authenticated:
    render_auth()
elif not st.session_state.profile_completed:
    render_profile_setup()
else:
    render_main_app()