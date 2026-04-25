import streamlit as st
from openai import OpenAI

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS ------------------ #
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
}

/* Header styling */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Chat bubbles */
.user-msg {
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    padding: 12px;
    border-radius: 12px;
    color: white;
    margin-bottom: 10px;
    animation: fadeIn 0.3s ease-in-out;
}

.assistant-msg {
    background: #1e293b;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 10px;
    animation: fadeIn 0.3s ease-in-out;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 8px;
    border: none;
}

/* Input box */
input {
    border-radius: 10px !important;
}

/* Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------ #
st.sidebar.title("🔐 Configuration")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Paste your API key here"
)

st.sidebar.markdown("""
---
### ⚙️ Settings
- Model: GPT-4o-mini  
- Mode: Smart Assistant  
- UI: Pro Theme  

---
### 📌 Tips
- Ask coding questions  
- Request ML models  
- Debug errors  
""")

# ------------------ HEADER ------------------ #
st.markdown('<div class="main-title">🤖 AI Assistant Pro</div>', unsafe_allow_html=True)
st.caption("🚀 Advanced AI for Coding, ML & Cybersecurity")

# ------------------ SESSION ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ DISPLAY CHAT ------------------ #
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg">🧑‍💻 {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-msg">🤖 {message["content"]}</div>', unsafe_allow_html=True)

# ------------------ INPUT ------------------ #
user_input = st.chat_input("💬 Ask anything...")

if user_input:
    if not api_key:
        st.warning("⚠️ Please enter API key")
        st.stop()

    client = OpenAI(api_key=api_key)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show instantly
    st.markdown(f'<div class="user-msg">🧑‍💻 {user_input}</div>', unsafe_allow_html=True)

    system_prompt = """
    You are an expert AI assistant in:
    - Machine Learning
    - Data Science
    - Cybersecurity
    - Python

    Give clear, structured, and practical answers.
    """

    with st.spinner("🤖 Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
                temperature=0.7
            )

            reply = response.choices[0].message.content

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display response
    st.markdown(f'<div class="assistant-msg">🤖 {reply}</div>', unsafe_allow_html=True)