import streamlit as st
from openai import OpenAI
import uuid

# ──────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="ChatGPT",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS — ChatGPT-style dark theme
# ──────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-primary: #212121;
    --bg-secondary: #171717;
    --bg-sidebar: #171717;
    --bg-input: #303030;
    --bg-hover: #2f2f2f;
    --text-primary: #ececec;
    --text-secondary: #b4b4b4;
    --text-muted: #8e8e8e;
    --accent: #10a37f;
    --accent-hover: #1a7f64;
    --border: #383838;
    --user-bubble: #303030;
    --code-bg: #1e1e1e;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 14px !important;
    transition: background-color 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: var(--bg-hover) !important;
}

/* ── chat messages ── */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 12px 0 !important;
    max-width: 768px !important;
    margin: 0 auto !important;
    font-size: 16px !important;
    line-height: 1.75 !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: var(--text-primary) !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
}
[data-testid="stChatMessage"] code {
    background-color: var(--code-bg) !important;
    color: #e6e6e6 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-size: 14px !important;
}
[data-testid="stChatMessage"] pre {
    background-color: var(--code-bg) !important;
    border-radius: 8px !important;
    padding: 16px !important;
    border: 1px solid var(--border) !important;
}

/* Chat input area */
[data-testid="stChatInput"] {
    max-width: 768px !important;
    margin: 0 auto !important;
}
[data-testid="stChatInput"] textarea {
    background-color: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    font-size: 16px !important;
    caret-color: var(--text-primary) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--text-secondary) !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] button {
    background-color: var(--text-primary) !important;
    border-radius: 10px !important;
}

/* ── selectbox ── */
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
    background-color: var(--bg-input) !important;
    border-radius: 8px !important;
}

/* ── Markdown styling ── */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text-primary) !important;
}
.stMarkdown a {
    color: var(--accent) !important;
}

/* ── conversation list buttons ── */
.chat-history-btn > button {
    background-color: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 14px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
.chat-history-btn > button:hover {
    background-color: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}
.active-chat > button {
    background-color: var(--bg-hover) !important;
    color: var(--text-primary) !important;
}

/* ── bottom container ── */
[data-testid="stBottomBlockContainer"] {
    background-color: var(--bg-primary) !important;
    padding-bottom: 1rem !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Warning/info boxes */
.stAlert { background-color: var(--bg-input) !important; color: var(--text-primary) !important; border-radius: 8px !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Available models
# ──────────────────────────────────────────────
MODELS = {
    "GPT-4.1 mini": "openai",
    "GPT-4.1": "openai-large",
    "Llama 3.3 70B": "llama",
    "Mistral Large": "mistral-large",
    "DeepSeek V3": "deepseek",
    "DeepSeek R1": "deepseek-r1",
}
DEFAULT_MODEL = "GPT-4.1 mini"

SYSTEM_PROMPT = (
    "You are ChatGPT, a large language model trained by OpenAI. "
    "Follow the user's instructions carefully. Respond using markdown when appropriate. "
    "Be concise yet thorough."
)

# ──────────────────────────────────────────────
# Session-state initialisation
# ──────────────────────────────────────────────
if "conversations" not in st.session_state:
    st.session_state.conversations = {}  # id -> {title, messages, model}

if "active_id" not in st.session_state:
    st.session_state.active_id = None


def _new_conversation(model_key: str = DEFAULT_MODEL) -> str:
    """Create a fresh conversation and return its id."""
    cid = str(uuid.uuid4())
    st.session_state.conversations[cid] = {
        "title": "New chat",
        "messages": [],
        "model": model_key,
    }
    st.session_state.active_id = cid
    return cid


def _get_active():
    """Return the active conversation dict, creating one if needed."""
    cid = st.session_state.active_id
    if cid is None or cid not in st.session_state.conversations:
        cid = _new_conversation()
    return st.session_state.conversations[cid]


def _auto_title(messages: list) -> str:
    """Derive a short title from the first user message."""
    for m in messages:
        if m["role"] == "user":
            text = m["content"].strip()
            return text[:40] + ("…" if len(text) > 40 else "")
    return "New chat"


# ──────────────────────────────────────────────
# Pollinations AI client (completely free, no API key)
# ──────────────────────────────────────────────
@st.cache_resource
def _get_client():
    """Return an OpenAI-compatible client pointed at Pollinations AI.
    Completely free — no API key, no sign-up, no rate-limit worries."""
    return OpenAI(
        base_url="https://text.pollinations.ai/openai",
        api_key="pollinations",  # required by SDK but not validated
    )


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    # Logo / brand
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:16px 0 8px 0;">
            <svg width="28" height="28" viewBox="0 0 41 41" fill="none"
                 xmlns="http://www.w3.org/2000/svg">
                <path d="M37.532 16.87a9.963 9.963 0 0 0-.856-8.184 10.078
                10.078 0 0 0-10.855-4.835A9.964 9.964 0 0 0 18.306.5a10.079
                10.079 0 0 0-9.614 6.977 9.967 9.967 0 0 0-6.664 4.834 10.08
                10.08 0 0 0 1.24 11.817 9.965 9.965 0 0 0 .856 8.185 10.079
                10.079 0 0 0 10.855 4.835 9.965 9.965 0 0 0 7.516 3.35 10.078
                10.078 0 0 0 9.617-6.981 9.967 9.967 0 0 0 6.663-4.834 10.079
                10.079 0 0 0-1.243-11.813ZM22.498 37.886a7.474 7.474 0 0
                1-4.799-1.735c.061-.033.168-.091.237-.134l7.964-4.6a1.294
                1.294 0 0 0 .655-1.134V19.054l3.366 1.944a.12.12 0 0 1
                .066.092v9.299a7.505 7.505 0 0 1-7.49 7.496ZM6.392
                31.006a7.471 7.471 0 0 1-.894-5.023c.06.036.162.099.237.141l7.964
                4.6a1.297 1.297 0 0 0 1.308 0l9.724-5.614v3.888a.12.12 0 0
                1-.048.103l-8.051 4.649a7.504 7.504 0 0
                1-10.24-2.744ZM4.297 13.62A7.469 7.469 0 0 1 8.2
                10.333c0 .068-.004.19-.004.274v9.201a1.294 1.294 0 0 0
                .654 1.132l9.723 5.614-3.366 1.944a.12.12 0 0 1-.114.012L7.044
                23.86a7.504 7.504 0 0 1-2.747-10.24Zm27.658
                6.437-9.724-5.615 3.367-1.943a.121.121 0 0 1
                .113-.012l8.051 4.649a7.498 7.498 0 0 1-1.158
                13.528v-9.476a1.293 1.293 0 0 0-.649-1.131Zm3.35-5.043c-.059-.037-.162-.099-.236-.141l-7.965-4.6a1.298
                1.298 0 0 0-1.308 0l-9.723 5.614v-3.888a.12.12 0 0 1
                .048-.103l8.05-4.645a7.497 7.497 0 0 1 11.135
                7.763Zm-21.063 6.929-3.367-1.944a.12.12 0 0
                1-.065-.092v-9.299a7.497 7.497 0 0 1
                12.293-5.756 6.94 6.94 0 0 0-.236.134l-7.965 4.6a1.294
                1.294 0 0 0-.654 1.132l-.006 11.225Zm1.829-3.943
                4.33-2.501 4.332 2.5v5l-4.331 2.5-4.331-2.5V18Z"
                fill="#ececec"/>
            </svg>
            <span style="font-size:18px;font-weight:600;color:#ececec;">
                ChatGPT
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # New-chat button
    if st.button("＋  New chat", use_container_width=True, key="new_chat"):
        _new_conversation()
        st.rerun()

    st.divider()

    # Model selector
    model_choice = st.selectbox(
        "Model",
        options=list(MODELS.keys()),
        index=list(MODELS.keys()).index(
            _get_active().get("model", DEFAULT_MODEL)
        ),
        key="model_selector",
    )
    _get_active()["model"] = model_choice

    st.divider()

    # Conversation history
    st.markdown(
        '<p style="font-size:12px;text-transform:uppercase;letter-spacing:0.05em;'
        'color:#8e8e8e;margin-bottom:4px;">Recent chats</p>',
        unsafe_allow_html=True,
    )
    for cid, conv_item in reversed(
        list(st.session_state.conversations.items())
    ):
        is_active = cid == st.session_state.active_id
        css_class = "active-chat" if is_active else "chat-history-btn"
        with st.container():
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            if st.button(
                conv_item["title"],
                key=f"conv_{cid}",
                use_container_width=True,
            ):
                st.session_state.active_id = cid
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Clear conversations
    if st.session_state.conversations:
        st.divider()
        if st.button(
            "🗑️  Clear all chats", use_container_width=True, key="clear"
        ):
            st.session_state.conversations = {}
            st.session_state.active_id = None
            st.rerun()

# ──────────────────────────────────────────────
# Main chat area
# ──────────────────────────────────────────────
conv = _get_active()
messages: list = conv["messages"]

# Welcome splash when conversation is empty
if not messages:
    st.markdown(
        """
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;height:50vh;text-align:center;">
            <svg width="48" height="48" viewBox="0 0 41 41" fill="none"
                 xmlns="http://www.w3.org/2000/svg" style="margin-bottom:20px;">
                <path d="M37.532 16.87a9.963 9.963 0 0 0-.856-8.184 10.078
                10.078 0 0 0-10.855-4.835A9.964 9.964 0 0 0 18.306.5a10.079
                10.079 0 0 0-9.614 6.977 9.967 9.967 0 0 0-6.664 4.834 10.08
                10.08 0 0 0 1.24 11.817 9.965 9.965 0 0 0 .856 8.185 10.079
                10.079 0 0 0 10.855 4.835 9.965 9.965 0 0 0 7.516 3.35 10.078
                10.078 0 0 0 9.617-6.981 9.967 9.967 0 0 0 6.663-4.834 10.079
                10.079 0 0 0-1.243-11.813Z" fill="#8e8e8e"/>
            </svg>
            <h2 style="color:#ececec;font-weight:600;margin:0;">
                How can I help you today?
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Render message history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Message ChatGPT…")

if prompt:
    # Add user message
    messages.append({"role": "user", "content": prompt})
    conv["title"] = _auto_title(messages)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    client = _get_client()
    with st.chat_message("assistant"):
        api_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in messages
        ]
        try:
            stream = client.chat.completions.create(
                model=MODELS[conv["model"]],
                messages=api_messages,
                stream=True,
            )
            response = st.write_stream(stream)
            messages.append(
                {"role": "assistant", "content": response}
            )
        except Exception as e:
            st.error(
                f"❌ Something went wrong. Please try again.\n\n"
                f"Details: {e}"
            )

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align:center;padding:8px 0 0 0;">
        <p style="font-size:12px;color:#8e8e8e;margin:0;">
            ChatGPT can make mistakes. Consider checking important
            information.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
