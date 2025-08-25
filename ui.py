from textwrap import dedent
import html
import streamlit as st
from components.styles import CYBER_CSS, PSYCHE_ASCII
from components.matrix import render_matrix_rain, MATRIX_CANVAS

# ==============================
# Utilities
# ==============================

def _escape_html(s: str) -> str:
    """Escape text for safe insertion into our HTML bubbles."""
    return html.escape(s or "", quote=True)

# ==============================
# Constants
# ==============================

NEON_BADGES = (
    "NEON",
    "GRID",
    "QUEST",
)

# ==============================
# Chat Helpers
# ==============================

def say_bot(text: str):
    """Append bot message to chat history."""
    st.session_state.chat.append(("bot", text))

def say_user(text: str):
    """Append user message to chat history."""
    st.session_state.chat.append(("user", text))

# ==============================
# Inventory / Session
# ==============================

def inventory_text() -> str:
    """Return inventory display string for fragments."""
    if not st.session_state.fragments:
        return "Fragments: [ none ]"
    return "Fragments: [ " + " ".join(st.session_state.fragments) + " ]"

def reset_run():
    """Reset game state (fresh session)."""
    st.session_state.chat = []
    st.session_state.stage = "intro"
    st.session_state.fragments = []
    st.session_state.hints_used = set()
    st.session_state.last_input = ""
    st.session_state.active_game = None
    st.session_state.docs_open = False
    st.session_state.puzzle_index = 0
    st.session_state.inventory_order = []

# ==============================
# UI Layers
# ==============================

def inject_global_styles():
    """Inject cyberpunk CSS theme."""
    st.markdown(CYBER_CSS, unsafe_allow_html=True)

def render_matrix_layers():
    """Render matrix rain and scanlines overlay."""
    render_matrix_rain()  # This will render the actual Matrix effect
    # Fallback static overlay
    st.markdown(MATRIX_CANVAS, unsafe_allow_html=True)

def render_header():
    st.markdown(
        f"""
<div class="header" style="text-align:center;">
  <pre><code class="psyche-ascii">{PSYCHE_ASCII}</code></pre>
  <div class="badges">
    <span class="badge">NEON</span>
    <span class="badge">GRID</span>
    <span class="badge">QUEST</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

def render_chat():
    """Messenger-style chat: bot on left, user on right."""
    rows = ["<div class='chat-container'>"]
    for role, text in st.session_state.chat:
        safe = _escape_html(str(text))
        if role == "bot":
            rows.append(
                "<div class='msg-row left'>"
                "<div class='avatar bot'>🤖</div>"
                f"<div class='bubble bot'>{safe}</div>"
                "</div>"
            )
        else:
            rows.append(
                "<div class='msg-row right'>"
                f"<div class='bubble user'>{safe}</div>"
                "<div class='avatar user'>🧑</div>"
                "</div>"
            )
    rows.append("</div>")
    st.markdown("\n".join(rows), unsafe_allow_html=True)

def render_docs_drawer():
    """Optional side drawer for in-app docs/help."""
    if not st.session_state.get("docs_open"):
        return
    st.markdown(
        """
<div class="docs-drawer">
  <h4>Docs</h4>
  <p>— Solve puzzles to assemble the Master Key.</p>
  <p>— Use 'hint', 'repeat', 'inventory' anytime.</p>
  <p>— Launch mini-games with 'game snake' or 'game typing'.</p>
</div>
""",
        unsafe_allow_html=True,
    )

def intro_boot():
    """Initial greeting on a fresh session."""
    if not st.session_state.chat:
        say_bot("Welcome, Operative. Type 'quest' to begin.")
