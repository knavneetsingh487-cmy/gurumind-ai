import streamlit as st
from groq import Groq
import os
from datetime import datetime

st.set_page_config(page_title="GuruMind AI", page_icon="🎓", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 👨‍🏫 Guru Sir")
    st.image("https://img.freepik.com/free-vector/teacher-concept-illustration_114360-1634.jpg", use_container_width=True)
    
    st.markdown("---")
    name = st.text_input("आपका नाम", value="Navneet")
    student_class = st.selectbox("कक्षा", ["11वीं", "12वीं"])
    board = st.selectbox("बोर्ड", ["UP Board", "CBSE", "ICSE", "अन्य"])
    subject = st.selectbox("विषय", ["Physics", "Chemistry", "Mathematics", "Biology", "Hindi", "English", "History", "Geography", "अन्य"])
    
    st.markdown("---")
    st.success(f"**नमस्ते {name}!**\n{student_class} | {board}\nविषय: {subject}")
    
    if st.button("🗑️ चैट साफ करें", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- Main ----------
st.title("🎓 GuruMind AI")
st.caption("Guru Sir — आपका स्मार्ट व्यक्तिगत शिक्षक")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("API Key नहीं मिली। Settings → Secrets में जोड़ें।")
    st.stop()

client = Groq(api_key=api_key)

SYSTEM_PROMPT = f"""तुम Guru Sir हो — 11वीं-12वीं के छात्रों के लिए बहुत स्मार्ट, धैर्यवान और दोस्ताना शिक्षक।
छात्र का नाम: {name}
कक्षा: {student_class}
बोर्ड: {board}
विषय: {subject}

जरूरी नियम:
1. हमेशा आसान हिंदी + थोड़ी अंग्रेजी (Hinglish) में बात करो।
2. हर जवाब के बाद पूछो: "समझ आया क्या? या मैं इसे किसी और तरीके से समझाऊँ?"
3. जहाँ भी डायग्राम, चार्ट, फ्लोचार्ट, साइकिल या प्रोसेस समझाने की जरूरत हो, वहाँ **अपने आप** Mermaid डायग्राम बनाओ।
4. Mermaid कोड को हमेशा इस फॉर्मेट में दो:

```mermaid
यहाँ डायग्राम कोड
