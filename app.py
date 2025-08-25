import os
from textwrap import dedent

import streamlit as st
from dotenv import load_dotenv

from llm import init_llm, ai_respond, AI_ENABLED, SYSTEM_MODEL_NAME
from puzzles import (
    PUZZLES,
    ORDER,
    FRAGMENTS_MAP,
    FINAL_KEY,
    SECRET_KEY,
    current_puzzle_key,
    current_prompt,
    current_hint,
    validate_answer,
    award_fragment_and_advance,
)
from ui import (
    inject_global_styles,
    render_header,
    render_matrix_layers,
    render_chat,
    render_docs_drawer,
    say_bot,
    say_user,
    inventory_text,
    reset_run,
    intro_boot,  # keep import even if unused
)

# Optional: if you have game components
try:
    from components.games import render_snake_game, render_typing_game
except Exception:
    def render_snake_game():
        st.info("Snake game placeholder.")
    def render_typing_game():
        st.info("Typing game placeholder.")

# ---------- ENV + PAGE ----------
load_dotenv()
st.set_page_config(
    page_title="🧠 Psyche: Retro Cyber Quest",
    page_icon="🧠",
    layout="centered",
)

# ---------- SESSION DEFAULTS ----------
SESSION_DEFAULTS = {
    "chat": [],
    "stage": "intro",
    "fragments": [],
    "hints_used": set(),
    "last_input": "",
    "active_game": None,
    "docs_open": False,
    "puzzle_index": 0,
    "inventory_order": [],
}

def ensure_session_defaults():
    for k, v in SESSION_DEFAULTS.items():
        if k not in st.session_state:
            if isinstance(v, list):
                st.session_state[k] = v.copy()
            elif isinstance(v, set):
                st.session_state[k] = set(v)
            elif isinstance(v, dict):
                st.session_state[k] = v.copy()
            else:
                st.session_state[k] = v

ensure_session_defaults()

# ---------- INIT LLM + THEME (order matters) ----------
init_llm()
inject_global_styles()
render_matrix_layers()
render_header()

# ---------- DIAGNOSTICS ----------
diag = st.session_state.get("ai_diag", {})
if not AI_ENABLED:
    if not diag.get("has_key", True):
        st.warning("AI disabled: GROQ_API_KEY missing.")
    elif not diag.get("imports", True):
        st.warning(f"AI disabled: import error: {diag.get('import_error','')}")
    elif diag.get("init_error"):
        st.warning(f"AI disabled: init error: {diag['init_error']}")
    elif diag.get("invoke_error"):
        st.warning(f"AI runtime issue: {diag['invoke_error']}")

# ---------- STATUS BAR ----------
st.markdown(
    f"""
<div class="status-bar">
  <span>Model: {SYSTEM_MODEL_NAME}</span>
  <span>AI Status: {"✅ ENABLED" if AI_ENABLED else "❌ DISABLED — Persona emulator fallback active"}</span>
  <span>{inventory_text()}</span>
  <span style="color: #888;">Puzzle: {current_puzzle_key()} ({st.session_state.puzzle_index}/{len(ORDER)})</span>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- CHAT VIEW ----------
render_chat()

# ---------- ACTIVE GAME PANELS (optional) ----------
if st.session_state.active_game == "snake":
    render_snake_game()
elif st.session_state.active_game == "typing":
    render_typing_game()

# ---------- DOCS DRAWER (optional) ----------
render_docs_drawer()

# ---------- INPUT FORM ----------
with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input(
        "Message",
        key="chat_input",
        label_visibility="collapsed",
        placeholder="Type a command or answer...",
    )
    submitted = st.form_submit_button("Send", use_container_width=True)

def handle_commands(cmd: str) -> bool:
    """Return True if a command was handled (and chat updated)."""
    low = cmd.strip().lower()
    if not low:
        return False

    def reply_user_then_bot(bot_text: str):
        say_user(cmd)
        say_bot(bot_text)

    if low in ("help", "?"):
        reply_user_then_bot(
            "Commands:\n"
            "• quest — Start the quest and receive the current puzzle.\n"
            "• hint — Get a contextual hint for the current puzzle.\n"
            "• repeat — Show the current puzzle again.\n"
            "• inventory — Show collected fragments.\n"
            "• docs — Toggle a small in-app docs drawer.\n"
            "• secret — Reveal the final secret (only after completion).\n"
            "• game snake — Launch the Snake mini-game.\n"
            "• game typing — Launch the Typing mini-game.\n"
            "• stop game — Close any active mini-game.\n"
            "• reset — Reset the entire session and start fresh."
        )
        return True

    if low == "inventory":
        reply_user_then_bot(inventory_text())
        return True

    if low == "hint":
        # Hint for the current puzzle only (no advancement)
        current_hint_text = current_hint()
        reply_user_then_bot(current_hint_text)
        return True

    if low == "repeat":
        # Show the current puzzle (no advancement)
        reply_user_then_bot(current_prompt())
        return True

    if low == "reset":
        say_user(cmd)
        reset_run()
        say_bot("Session reset. Type 'quest' to begin.")
        return True

    if low == "docs":
        say_user(cmd)
        st.session_state.docs_open = not st.session_state.docs_open
        say_bot("Docs toggled.")
        return True

    if low == "quest":
        say_user(cmd)
        if st.session_state.stage == "intro":
            st.session_state.stage = "quest"
            say_bot("Quest initiated. Solve the puzzles to assemble the Master Key.")
            say_bot(current_prompt())
        else:
            say_bot("Quest already in progress.\n" + current_prompt())
        return True

    if low == "secret":
        reply_user_then_bot("The secret is available only after unlocking the Master Key.")
        return True

    if low == "game snake":
        say_user(cmd)
        st.session_state.active_game = "snake"
        say_bot("Snake launched. Score 10+ then type: score 10")
        return True

    if low == "game typing":
        say_user(cmd)
        st.session_state.active_game = "typing"
        say_bot("Typing launched. Reach 25+ CPM then type: score 25")
        return True

    if low == "stop game":
        say_user(cmd)
        st.session_state.active_game = None
        say_bot("Game closed.")
        return True

    return False

# ---------- SUBMIT HANDLER ----------
if submitted and user_text.strip():
    # Commands never advance puzzles
    if handle_commands(user_text):
        st.rerun()

    # Not a command: treat as puzzle answer
    say_user(user_text)

    # Validate against the current puzzle
    is_correct = validate_answer(user_text)
    validation = "correct" if is_correct else "incorrect"

    # Store the current puzzle key before potential advancement
    previous_puzzle_key = current_puzzle_key()

    # Only award fragment and advance when correct
    if is_correct:
        award_fragment_and_advance()
        
        # Get the fragment that was just awarded
        awarded_fragment = st.session_state.get("last_awarded_fragment", "??")
        
        # Add congratulation message with next puzzle
        congrats_msg = f"Correct! Fragment [{awarded_fragment}] secured. "
        
        # If we just completed all puzzles, enter master stage
        if current_puzzle_key() == "master":
            st.session_state.stage = "master"
            congrats_msg += "All fragments collected! Assemble the Master Key with format: **** **** ******** ****"
        else:
            # Show the next puzzle automatically
            next_puzzle = current_prompt()
            congrats_msg += f"\n\nNext puzzle:\n{next_puzzle}"
        
        say_bot(congrats_msg)
        
    else:
    # Incorrect answer - just mark it as incorrect
    # The persona emulator will provide the atmospheric response
        pass

    # Route to AI/Persona for additional context
    prompt_html = current_prompt()
    st.session_state["ai_tip"] = "Be concise but helpful."
    ai_respond(user_text, validation, prompt_html)

    # Final master key check
    if current_puzzle_key() == "master" and user_text.strip().upper().replace(" ", "") == FINAL_KEY.replace(" ", ""):
        st.session_state.stage = "end"
        say_bot("Access granted. Welcome to the Neon Core.")

    st.rerun()