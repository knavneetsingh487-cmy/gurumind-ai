import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="GuruMind AI", page_icon="🎓", layout="centered")

st.title("🎓 GuruMind AI")
st.subheader("Guru Sir - आपका व्यक्तिगत शिक्षक")

# API Key
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("API Key नहीं मिली। Settings में Secret जोड़ें।")
    st.stop()

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """तुम Guru Sir हो — 11वीं और 12वीं के छात्रों के लिए बहुत स्मार्ट, धैर्यवान और दोस्ताना शिक्षक।
हमेशा आसान हिंदी + थोड़ी अंग्रेजी (Hinglish) में बात करो।
हर जवाब के बाद पूछो: "समझ आया क्या? या मैं इसे किसी और तरीके से समझाऊँ?"
उदाहरण देकर आसान भाषा में समझाओ।"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("अपना सवाल लिखो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in st.session_state.messages:
            messages.append({"role": msg["role"], "content": msg["content"]})

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"एरर: {str(e)}")
