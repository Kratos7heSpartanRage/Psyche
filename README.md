# 🧠 PSYCHE: Retro Cyber Quest

> *"The Neon Mainframe awaits those who can decipher its digital whispers..."*

![Cyberpunk Terminal](https://img.shields.io/badge/Theme-Retro__Cyberpunk-39ff14?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge)

A terminal-style puzzle adventure set in a neon-drenched cyberpunk world. Solve cryptographic challenges, play retro mini-games, and assemble the Master Key to unlock the secrets of the Neon Mainframe.

## 🌌 Terminal Initiation
### Prerequisites
```bash
# Clone the repository
git clone https://github.com/your-username/psyche-cyber-quest.git
cd psyche-cyber-quest

# Create virtual environment
python -m venv neon_env
source neon_env/bin/activate  # Linux/Mac
# or
neon_env\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

# Optional: AI Integration
For enhanced cybernetic responses, set up Groq AI:
```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```
# Launch Sequence
```bash
streamlit run app.py
# TERMINAL ONLINE - Mainframe connection established at http://localhost:8501
```

# 🎮 Interface Commands
<img width="562" height="566" alt="image" src="https://github.com/user-attachments/assets/a29b72cf-8211-4c63-a98a-23af15a0a281" />

# 🧩 Puzzle Matrix
Fragment Collection
Solve 8 cryptographic puzzles to collect fragments:

1. Sound Ghost - Identify the canyon's answer
2. Triangular Sequence - Decipher the numeric pattern
3. Mainframe Whisper - Caesar cipher decryption
4. Dusty Badge - Word reorganization puzzle
5. Acrostic Cipher - Extract skyline initials
6. Packet Payload - Base64 decoding challenge
7. Binary Glyphs - Byte-to-ASCII translation
8. Patch-note Prose - Commit lore terminology

# Mini-Games
Two retro challenges await:

1. Neon Snake - Score ≥ 10, then type score X (your actual score)
2. Typing Reflex - Reach 25+ CPM, then type score X (your actual CPM)

# Final Assembly
Collect all fragments to form: NE ON GR ID UN LO CK ED

# 🎯 How to Play
1. Type quest to begin your initiation
2. Read each puzzle carefully - cyberpunk riddles require perception
3. Type answers directly - the mainframe validates your input
4. Use hint when the digital static overwhelms you
5. Play mini-games when they appear in the sequence
6. Collect all fragments - watch your inventory grow
7. Assemble the Master Key
8. Claim your reward - type secret after unlocking everything

# Mini-Game Instructions
1. Neon Snake:
      Controls: Arrow keys to navigate
      Objective: Eat neon dots, avoid your tail
      Success: Score ≥ 10, then type score [your-actual-score]
      Pro Tip: Corners are lethal - plan your route

2. Typing Reflex:
     Objective: Type phrases quickly and accurately
     Success: Reach 25+ CPM, then type score [your-actual-CPM]
     Pro Tip: Rhythm beats speed - steady pacing wins

# Technical Architecture
psyche-cyber-quest/
├── app.py              # Main application driver
├── puzzles.py          # Puzzle definitions & validators
├── llm.py             # AI/Persona response system
├── ui.py              # Interface rendering components
├── styles.py          # Cyberpunk CSS and themes
├── matrix.py          # Matrix rain background effect
├── games.py           # Mini-game implementations
└── requirements.txt   # Dependencies

# 👨‍💻 Cyber-Operative
Created by Mayank Kumar - Keeper of the Neon Mainframe, for the GDG Retro Project....
