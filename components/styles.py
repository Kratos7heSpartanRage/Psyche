import streamlit as st
from textwrap import dedent

NEON_COLORS = {
    "bg": "#06080b",
    "fg": "#27ffb8",
    "accent": "#0df",
    "magenta": "#ff00ff",
    "purple": "#a64dff",
}

FONT_MONO = '"JetBrains Mono","Fira Code",ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace'

CYBER_CSS = f"""
<style>
:root {{
  --neon: {NEON_COLORS["fg"]};
  --neon2: {NEON_COLORS["accent"]};
  --bg: {NEON_COLORS["bg"]};
  --panel: rgba(255,255,255,0.03);
  --border: rgba(255,255,255,0.08);
  --text: #d5e9f7;
  --chat-font: {FONT_MONO};
}}

html, body, [data-testid="stAppViewContainer"] {{
  background: transparent !important;
}}

.header {{
  margin: 10px 0 6px 0;
  text-align: center;
}}

.psyche-ascii {{
  font-family: "Courier New", monospace;
  font-size: 14px;
  white-space: pre;
  display: inline-block;
  margin: 0 auto;
  color: var(--neon);
  mix-blend-mode: screen;       /* ✅ blend with rain behind */
  text-shadow: 0 0 8px rgba(39,255,184,0.8),
               0 0 16px rgba(13,255,255,0.5);
}}

.badges {{ display:flex; gap:8px; justify-content:center; margin-top:6px; }}
.badge {{
  border:1px solid var(--border); background: var(--panel);
  color: var(--neon2); padding: 2px 8px; border-radius: 10px;
  font-family: var(--chat-font); font-size: 12px;
}}

.status-bar {{
  display:flex; gap: 12px; justify-content: space-between; align-items:center;
  border:1px solid var(--border); background: var(--panel);
  padding: 6px 10px; border-radius: 10px; margin-bottom: 10px;
  color: var(--text); font-family: var(--chat-font);
}}

.chat-container {{
  width: 100%; display: flex; flex-direction: column; gap: 12px;
  font-family: var(--chat-font); font-size: 14px;
}}
.msg-row {{ display: flex; align-items: flex-end; }}
.msg-row.left {{ justify-content: flex-start; }}
.msg-row.right {{ justify-content: flex-end; }}

.avatar {{
  width: 28px; height: 28px; border-radius: 50%;
  display:flex; align-items:center; justify-content:center;
  background:#111; color: var(--neon); margin: 0 8px; font-size:14px;
  border:1px solid var(--border);
}}

.bubble {{
  max-width: 70%; padding: 10px 12px; border-radius: 14px; line-height: 1.45;
  border:1px solid var(--border); background: var(--panel);
  color: var(--text); white-space: pre-wrap; word-wrap: break-word;
}}
.bubble.bot {{
  background: rgba(0,255,170,0.08); border: 1px solid rgba(0,255,170,0.35);
  color:#c8ffe6; border-top-left-radius: 4px; text-align: left;
}}
.bubble.user {{
  background: rgba(0,136,255,0.12); border: 1px solid rgba(0,136,255,0.4);
  color:#e0f0ff; border-top-right-radius: 4px; text-align: right;
}}

.docs-drawer {{
  position: sticky; top: 10px; margin-top: 8px;
  border:1px solid var(--border); background: var(--panel);
  padding: 10px; border-radius: 10px; color: var(--text);
  font-family: var(--chat-font);
}}

[data-testid="stTextInputRoot"] > div > input {{
  font-family: var(--chat-font);
}}
</style>
"""

PSYCHE_ASCII = r"""
██████╗ ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗
██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██║  ██║██╔════╝
██████╔╝███████╗ ╚████╔╝ ██║     ███████║█████╗  
██╔═══╝ ╚════██║  ╚██╔╝  ██║     ██╔══██║██╔══╝  
██║     ███████║   ██║   ╚██████╗██║  ██║███████╗
╚═╝     ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝
"""

