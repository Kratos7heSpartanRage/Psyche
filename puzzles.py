import re
import streamlit as st

# ==============================
# Constants
# ==============================

FINAL_KEY = "NEON GRID UNLOCKED"
SECRET_KEY = "PSY-KEY"

# ==============================
# Puzzle Definitions
# ==============================

PUZZLES = [
    {
        "key": "p1",
        "fragment": "NE",
        "prompt": "Signal without source. No lungs, no lips—yet the canyon answers when the wind carries it. Identify the ghost of sound.",
        "hint": "When you shout in a canyon, what answers back?",
        "validator": lambda s: "echo" in s.lower().strip(),
    },
    {
        "key": "p2",
        "fragment": "ON",
        "prompt": "Triangular surge (Observe the sequence): 2, 6, 12, 20, 30, __? Observe the delta ladder: +4, +6, +8, +10 → next.",
        "hint": "Next jump equals to the number of units in a dozen.",
        "validator": lambda s: s.strip().isdigit() and int(s.strip()) == 42,
    },
    {
        "key": "p3",
        "fragment": "GR",
        "prompt": "Mainframe whisper: 'julg'. Apply Caesar shift -3. Surface the lattice that maps the city.",
        "hint": "J→G, U→R, L→I, G→D.",
        "validator": lambda s: s.lower().strip() == "grid",
    },
    {
        "key": "p4",
        "fragment": "ID",
        "prompt": "Dust off the badge from before the neon dawn: T O R E R → reorganize to the old-school sigil.",
        "hint": "The counterword of 'modern'.",
        "validator": lambda s: s.lower().replace(" ", "") == "retro",
    },
    {
        "key": "p5",
        "fragment": "UN",
        "prompt": (
            "Acrostic:\n"
            "Under neon rain, terminals sing,\n"
            "Narrow alleys hum with code,\n"
            "Loose packets hitch on midnight winds,\n"
            "Obsidian screens breathe static snow,\n"
            "Ciphers bloom like city lights,\n"
            "Keep your eyes on edges—secrets grow.\n"
            "Extract the skyline initials."
        ),
        "hint": "Take the first letter of each line.",
        "validator": lambda s: s.lower().strip() == "unlock",
    },
    {
        "key": "p6",
        "fragment": "LO",
        "prompt": "Packet payload inbound: bG9jaw==. Decode the base; name the latch.",
        "hint": "Use a Base64 decoder.",
        "validator": lambda s: s.lower().strip() == "lock",
    },
    {
        "key": "p7",
        "fragment": "CK",
        "prompt": "Two bytes, two glyphs: 01000011 01001011 → translate from base-2 to terminal ink.",
        "hint": "Split bytes, base-2 → decimal → ASCII.",
        "validator": lambda s: s.lower().strip() == "ck",
    },
    {
        "key": "p8",
        "fragment": "ED",
        "prompt": "Patch-note prose: past tense of 'edit' in commit lore? Keep it clean like a tidy diff.?",
        "hint": "Add -ed.",
        "validator": lambda s: s.lower().strip() == "edited",
    },
    {
        "key": "snake",
        "fragment": "20",
        "prompt": "Mini-game: Neon Snake. Type 'game snake' to open it. Open the grid, dance past your tail, and log your brag. Score at least 10 and then type 'score 10' (or higher).",
        "hint": "Keep your tail short; corners bite. Claim with: score 12",
        "validator": lambda s: (m := re.search(r"score\s+(\d+)", s.lower())) and int(m.group(1)) >= 10,
    },
    {
        "key": "typing",
        "fragment": "25",
        "prompt": "Neon Typing Reflex: Type 'game typing' to start. Stream pure keys, no panic—steady clocking wins. Reach 25 CPM+ and type 'score 25'.",
        "hint": "Rhythm beats speed. Claim with: score 25",
        "validator": lambda s: (m := re.search(r"score\s+(\d+)", s.lower())) and int(m.group(1)) >= 25,
    },
]

ORDER = [p["key"] for p in PUZZLES]
FRAGMENTS_MAP = {p["key"]: p["fragment"] for p in PUZZLES}

# ==============================
# Helpers
# ==============================

def current_puzzle_key():
    idx = st.session_state.puzzle_index
    if idx < len(ORDER):
        return ORDER[idx]
    return "master"

def current_prompt():
    key = current_puzzle_key()
    if key == "master":
        return "Assemble all shards into the Master Key with format: ** ** ****"
    puzzle = next(p for p in PUZZLES if p["key"] == key)
    return puzzle["prompt"]

def current_hint():
    key = current_puzzle_key()
    if key == "master":
        return "You know the phrase by now. Mind the spaces."
    puzzle = next(p for p in PUZZLES if p["key"] == key)
    return puzzle["hint"]

def validate_answer(user_text: str):
    key = current_puzzle_key()
    if key == "master":
        attempt = user_text.strip().upper().replace(" ", "")
        return attempt == FINAL_KEY.replace(" ", "")
    puzzle = next(p for p in PUZZLES if p["key"] == key)
    return bool(puzzle["validator"](user_text))

def award_fragment_and_advance():
    key = current_puzzle_key()
    if key == "master":
        return
    frag = FRAGMENTS_MAP[key]
    if frag not in st.session_state.fragments:
        st.session_state.fragments.append(frag)
        st.session_state.inventory_order.append(frag)
        st.session_state.puzzle_index += 1
    # Auto-close mini-game panel if leaving a game stage
    if st.session_state.active_game and key in ("snake", "typing"):
        st.session_state.active_game = None
