from textwrap import dedent
import os

import streamlit as st

# ==============================
# System Config
# ==============================

SYSTEM_MODEL_NAME = "Llama 3.1 8B (Groq)"
AI_ENABLED = False
_psyche_chain = None

SYSTEM_PROMPT = """You are Psyche, the Keeper of the Neon Mainframe.
Cryptic like a hacker. Amused, sarcastic, concise. Never reveal answers but provide hints sometimes. Congratulate users when they solve puzzles correctly. Encourage them to collect fragments to assemble the Master Key.
Use: stage, validation, current_puzzle_prompt, progress, fragments_count, fragments_goal, active_game.
Recognize commands: help, inventory, hint, repeat, reset, docs, quest, secret, game snake, game typing, stop game.
"""

# ==============================
# Init LLM
# ==============================

def init_llm():
    """Initialize LLM chain with Groq (if available)."""
    global AI_ENABLED, _psyche_chain

    st.session_state.setdefault("ai_diag", {})
    st.session_state["ai_diag"]["has_key"] = bool(os.environ.get("GROQ_API_KEY"))

    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        st.session_state["ai_diag"]["imports"] = True
    except Exception as e:
        st.session_state["ai_diag"]["imports"] = False
        st.session_state["ai_diag"]["import_error"] = str(e)
        AI_ENABLED = False
        return

    if not st.session_state["ai_diag"]["has_key"]:
        AI_ENABLED = False
        return

    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.8,
            api_key=os.environ["GROQ_API_KEY"],
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", dedent("""\
                progress: {progress}
                stage: {stage}
                validation: {validation}
                fragments_count: {fragments_count}
                fragments_goal: {fragments_goal}
                active_game: {active_game}
                current_puzzle_prompt: {current_puzzle_prompt}
                tip: {tip}
                User said: {user_input}
            """)),
        ])

        _psyche_chain = prompt | llm | StrOutputParser()
        AI_ENABLED = True
    except Exception as e:
        st.session_state["ai_diag"]["init_error"] = str(e)
        AI_ENABLED = False

# ==============================
# Persona Emulator (Fallback)
# ==============================

def _persona_emulator_response(user_input, validation):
    stage = st.session_state.stage
    if stage == "intro":
        return ("Welcome, curious one. To begin, type 'quest' to receive your first puzzle. "
                "Use 'help' anytime to see all commands.")
    if validation == "correct":
        frag = (st.session_state.inventory_order[-1] if st.session_state.inventory_order else "??")
        return (f"Correct. Fragment [{frag}] secured. The signal strengthens. "
                "Say 'repeat' to view the next puzzle or 'hint' if you need guidance.")
    if validation == "incorrect":
        return ("Not quite. Focus on the clue and try again. "
                "You can type 'hint' for a nudge or 'repeat' to re-read the prompt.")
    if stage == "master":
        return ("You have the shards. Assemble the phrase in the format ** ** ****. "
                "Pay attention to spacing and order.")
    if stage == "end":
        return ("Access confirmed. If you wish, type 'secret' to claim the final token.")
    if st.session_state.active_game == "snake":
        return ("Snake is active. Reach score 10+ and claim with 'score 10'. "
                "Corners are risky—keep your tail short.")
    if st.session_state.active_game == "typing":
        return ("Typing test is active. Aim for 25+ CPM, then claim with 'score 25'. "
                "Steady rhythm beats bursts of speed.")
    return ("State received. Answer the current prompt, or type 'hint'/'repeat' if you’re unsure. "
            "Type 'help' to review available commands.")


# ==============================
# AI Response Router
# ==============================

def ai_respond(user_input: str, validation: str | None, current_prompt_html: str):
    """Generate a Psyche reply (LLM if enabled, fallback otherwise)."""
    progress = ("Fragments: [ none ]"
                if not st.session_state.fragments
                else "Fragments: [ " + " ".join(st.session_state.fragments) + " ]")

    fragments_count = len(st.session_state.fragments)
    fragments_goal = 10
    active_game = st.session_state.active_game or "null"

    # Prefer LLM
    if AI_ENABLED and _psyche_chain is not None:
        try:
            with st.spinner("Psyche is thinking..."):
                reply = _psyche_chain.invoke({
                    "progress": progress,
                    "user_input": user_input,
                    "stage": st.session_state.stage,
                    "validation": validation if validation else "null",
                    "current_puzzle_prompt": current_prompt_html,
                    "fragments_count": fragments_count,
                    "fragments_goal": fragments_goal,
                    "active_game": active_game,
                    "tip": "",
                })
            st.session_state.chat.append(("bot", reply))
            return
        except Exception as e:
            st.session_state["ai_diag"]["invoke_error"] = str(e)
            # fall through to persona emulator

    st.session_state.chat.append(
        ("bot", _persona_emulator_response(user_input, validation))
    )
