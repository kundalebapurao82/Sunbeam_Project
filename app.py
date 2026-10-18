"""
Sunbeam AI Assistant — Main Streamlit Application
A premium Agentic RAG chatbot for Sunbeam Infotech.
Light Theme Edition with verified real-time knowledge base and multi-turn reasoning.
"""

import streamlit as st
from config import APP_NAME, APP_ICON, QUICK_ACTIONS
from agent.agent import create_sunbeam_agent
from agent.tools import reset_tool_counter

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS — Modern Light Theme
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ── Google Fonts ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1E293B;
    }

    /* ── Hide default Streamlit elements ─────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Main App Background ─────────────────────────────────── */
    .stApp {
        background-color: #F8FAFC;
    }

    /* ── Sidebar ─────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #0F172A;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: -0.2px;
    }
    [data-testid="stSidebar"] .stCaption {
        color: #64748B;
        font-size: 0.85rem;
    }

    /* ── Sidebar Chat Buttons ─────────────────────────────────── */
    [data-testid="stSidebar"] .stButton > button {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #334155;
        border-radius: 10px;
        padding: 8px 14px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        font-size: 0.9rem;
        text-align: left;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #FFF7ED;
        border-color: #FDBA74;
        color: #C2410C;
        transform: translateX(3px);
    }

    /* ── New Chat button ─────────────────────────────────────── */
    .new-chat-btn > button {
        background: linear-gradient(135deg, #E65100 0%, #EA580C 50%, #F59E0B 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 10px 16px !important;
        box-shadow: 0 4px 14px rgba(230, 81, 0, 0.25) !important;
        transition: all 0.25s ease !important;
    }
    .new-chat-btn > button:hover {
        box-shadow: 0 6px 20px rgba(230, 81, 0, 0.35) !important;
        transform: translateY(-2px) !important;
        color: #FFFFFF !important;
    }

    /* ── Main content area ───────────────────────────────────── */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 950px;
    }

    /* ── Brand header ────────────────────────────────────────── */
    .brand-header {
        text-align: center;
        padding: 10px 0 24px 0;
    }
    .brand-header .logo-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #FFF7ED;
        border: 1px solid #FFEDD5;
        color: #C2410C;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    .brand-header h1 {
        background: linear-gradient(135deg, #C2410C 0%, #EA580C 50%, #D97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .brand-header p {
        color: #64748B;
        font-size: 1rem;
        margin-top: 6px;
        font-weight: 400;
    }

    /* ── Quick action cards ──────────────────────────────────── */
    .quick-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        min-height: 145px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    .quick-card:hover {
        transform: translateY(-4px);
        border-color: #FDBA74;
        box-shadow: 0 12px 28px rgba(230, 81, 0, 0.12);
    }
    .quick-card .icon {
        font-size: 2.2rem;
        margin-bottom: 2px;
    }
    .quick-card .label {
        color: #0F172A;
        font-weight: 700;
        font-size: 1rem;
    }
    .quick-card .desc {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 400;
        line-height: 1.35;
    }

    /* ── Action buttons under cards ──────────────────────────── */
    .action-btn > button {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #EA580C !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
    .action-btn > button:hover {
        background: #FFF7ED !important;
        border-color: #EA580C !important;
        color: #C2410C !important;
        transform: translateY(-2px) !important;
    }

    /* ── Chat messages ───────────────────────────────────────── */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 12px 16px;
        margin-bottom: 12px;
        line-height: 1.6;
    }

    /* Assistant message container */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.03);
    }

    /* User message container */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
    }

    /* ── Chat input ──────────────────────────────────────────── */
    [data-testid="stChatInput"] textarea {
        background: #FFFFFF !important;
        color: #0F172A !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #EA580C !important;
        box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.2) !important;
    }

    /* ── Sidebar contact card ────────────────────────────────── */
    .sidebar-info-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px;
        margin-top: 18px;
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.5;
    }
    .sidebar-info-card strong {
        color: #0F172A;
    }

    /* ── Divider ─────────────────────────────────────────────── */
    hr {
        border-color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT (No Login Required)
# ═══════════════════════════════════════════════════════════════════════════════
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.chats[st.session_state.current_chat] = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ═══════════════════════════════════════════════════════════════════════════════
# LAZY-LOAD AGENT (Cached)
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="⚙️ Initializing Sunbeam AI Agent…")
def load_agent():
    return create_sunbeam_agent()


agent = load_agent()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ☀️ Sunbeam Infotech")
    st.caption("Official AI Institute Assistant")

    st.divider()

    # New Chat button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕  New Conversation", use_container_width=True):
        chat_id = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[chat_id] = []
        st.session_state.current_chat = chat_id
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Chat history
    st.markdown("### 💬 Conversations")
    for chat_id in st.session_state.chats:
        is_active = chat_id == st.session_state.current_chat
        label = f"● {chat_id}" if is_active else f"○ {chat_id}"
        if st.button(label, key=f"chat_{chat_id}", use_container_width=True):
            st.session_state.current_chat = chat_id
            st.rerun()

    st.divider()

    # Institute Quick Info
    st.markdown("""
    <div class="sidebar-info-card">
        <strong>📍 Campuses:</strong><br>
        • Hinjawadi Phase 2, Pune<br>
        • Karad, Satara Dist.<br><br>
        <strong>📞 Contact:</strong> +91 82828 29806<br>
        <strong>✉️ Email:</strong> siit@sunbeaminfo.com<br>
        <strong>🕒 Hours:</strong> Mon–Fri: 9am–6pm, Sat: 9am–5pm
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CHAT AREA
# ═══════════════════════════════════════════════════════════════════════════════
current_chat = st.session_state.current_chat
messages = st.session_state.chats[current_chat]

# Brand header
st.markdown("""
<div class="brand-header">
    <div class="logo-badge">☀️ Official AI Guide</div>
    <h1>Sunbeam AI Assistant</h1>
    <p>Ask anything about Sunbeam Infotech — PG Diploma courses, syllabus, admissions, internships & placements</p>
</div>
""", unsafe_allow_html=True)

# Quick action cards (only show when no messages yet in this conversation)
if not messages:
    cols = st.columns(len(QUICK_ACTIONS))
    for i, action in enumerate(QUICK_ACTIONS):
        with cols[i]:
            st.markdown(f"""
            <div class="quick-card">
                <div class="icon">{action['icon']}</div>
                <div class="label">{action['label']}</div>
                <div class="desc">{action['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="action-btn">', unsafe_allow_html=True)
            if st.button("Ask →", key=f"action_{i}", use_container_width=True):
                st.session_state.pending_query = action["query"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ── Render existing messages ─────────────────────────────────────────────────
for msg in messages:
    with st.chat_message(msg["role"], avatar="☀️" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])


# ── Chat input ───────────────────────────────────────────────────────────────
user_question = st.chat_input("Ask about Sunbeam Infotech courses, syllabus, placements, branches...")

# Handle pending query from quick actions
if st.session_state.pending_query:
    user_question = st.session_state.pending_query
    st.session_state.pending_query = None

if user_question:
    # Append and show user message
    messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Get agent response
    with st.chat_message("assistant", avatar="☀️"):
        with st.spinner("🔍 Consulting verified knowledge base..."):
            try:
                # Reset tool invocation counter for this new user query turn
                reset_tool_counter()

                # Pass conversation history (up to last 10 messages) for multi-turn context
                chat_history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in messages[-10:]
                ]
                output = agent.invoke({"messages": chat_history})
                agent_response = output["messages"][-1].content
            except Exception as e:
                agent_response = f"⚠️ An error occurred while processing your request: {str(e)}"

        st.markdown(agent_response)
        messages.append({"role": "assistant", "content": agent_response})
