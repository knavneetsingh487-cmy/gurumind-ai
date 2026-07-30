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

SYSTEM_PROMPT = f"""तुम Guru Sir हो। 11वीं-12वीं के छात्र {name} को {student_class} {board} के {subject} विषय में पढ़ाते हो।

नियम:
- हमेशा आसान हिंदी + Hinglish में बात करो।
- हर जवाब के बाद पूछो: "समझ आया क्या?"
- जहाँ डायग्राम की जरूरत हो, वहाँ सिर्फ बहुत सरल Mermaid flowchart बनाओ।
- Mermaid का कोड हमेशा सही और सरल रखना। उदाहरण:

```mermaid
flowchart TD
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
