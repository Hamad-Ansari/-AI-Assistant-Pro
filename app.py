import streamlit as st
from openai import OpenAI

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #6366f1, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* Chat Cards */
.user-box {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    color: white;
}

.bot-box {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    color: #f8fafc;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #22c55e);
    color: white;
    border-radius: 10px;
    border: none;
}

/* Inputs */
input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("🔐 Configuration")

api_key = st.sidebar.text_input(
    "Enter OpenAI API Key",
    type="password"
)

st.sidebar.markdown("""
---
### ⚙️ Model Settings
- Model: `gpt-4o-mini`
- Theme: Dark Pro
- Response: Smart Mode

---
### 📌 Tips
- Ask coding questions  
- Ask ML / AI questions  
- Ask cybersecurity topics  
""")

# ======================================================
# HEADER
# ======================================================
st.markdown('<p class="main-title">🤖 AI Assistant Pro</p>', unsafe_allow_html=True)
st.caption("🚀 Built with Streamlit & OpenAI")

# ======================================================
# SESSION STATE
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================================
# DISPLAY CHAT HISTORY
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
        st.warning("⚠️ Please enter your OpenAI API key in sidebar.")
        st.stop()

    # Show user instantly
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    st.markdown(
        f'<div class="user-box">🧑 {prompt}</div>',
        unsafe_allow_html=True
    )

    # Create client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error("❌ Invalid API Key")
        st.stop()

    # System prompt
    system_prompt = """
You are a professional AI assistant specialized in:

- Python Programming
- Machine Learning
- Data Science
- Cybersecurity

Always provide:
- Clear answers
- Structured responses
- Practical solutions
- Clean code examples
"""

    # Prepare messages
    messages = [{"role": "system", "content": system_prompt}]

    for m in st.session_state.messages:
        messages.append({
            "role": m["role"],
            "content": m["content"]
        })

    # Generate Response
    with st.spinner("🤖 Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=700
            )

            reply = response.choices[0].message.content

        except Exception as e:
            st.error(f"❌ API Error: {e}")
            st.stop()

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    # Show assistant response
    st.markdown(
        f'<div class="bot-box">🤖 {reply}</div>',
        unsafe_allow_html=True
    )
