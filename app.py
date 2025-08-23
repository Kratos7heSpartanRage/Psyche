import streamlit as st

st.title("Psyche: Retro Cyber Chatbot")

user_input = st.text_input("Say something to Psyche:")

if user_input:
    user_input_lower = user_input.lower()
    if user_input_lower in ['hello', 'hi', 'hey']:
        response = "Salutations, netrunner. The city pulses under neon veins. Ask what you seek."
    else:
        response = "I do not understand... try another command."
    st.write("Psyche:", response)
