import streamlit as st
import google.generativeai as genai

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Assistant Pro - Gemini",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #6366f1, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* User Chat */
.user-box {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    color: white;
}

/* Bot Chat */
.bot-box {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    color: #f8fafc;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("🔐 Configuration")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

st.sidebar.markdown("""
---
### ⚙️ Settings
- Model: Gemini 1.5 Flash
- Fast & Free
- Smart Assistant Mode

---
### 📌 Tips
- Ask Python questions
- Ask ML questions
- Ask Cybersecurity topics
""")

# ======================================================
# HEADER
# ======================================================
st.markdown(
    '<p class="main-title">🤖 AI Assistant Pro</p>',
    unsafe_allow_html=True
)
st.caption("🚀 Powered by Google Gemini")

# ======================================================
# SESSION STATE
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================================
# SHOW CHAT HISTORY
# ======================================================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-box">🧑 {msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-box">🤖 {msg["content"]}</div>',
            unsafe_allow_html=True
        )

# ======================================================
# CHAT INPUT
# ======================================================
prompt = st.chat_input("💬 Ask me anything...")

if prompt:

    if not api_key:
        st.warning("⚠️ Please enter Gemini API key.")
        st.stop()

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    st.markdown(
        f'<div class="user-box">🧑 {prompt}</div>',
        unsafe_allow_html=True
    )

    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except:
        st.error("❌ Invalid API key.")
        st.stop()

    # Create context
    history = """
You are an expert AI assistant specialized in:

- Python Programming
- Machine Learning
- Data Science
- Cybersecurity

Provide:
- Clear explanations
- Practical solutions
- Structured answers
- Clean code
"""

    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"\n{role}: {msg['content']}"

    # Generate response
    with st.spinner("🤖 Thinking..."):
        try:
            response = model.generate_content(history)
            reply = response.text

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

    # Save bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # Show response
    st.markdown(
        f'<div class="bot-box">🤖 {reply}</div>',
        unsafe_allow_html=True
    )