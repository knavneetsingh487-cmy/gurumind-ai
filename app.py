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
3. जहाँ भी डायग्राम, चार्ट, फ्लोचार्ट, साइकिल या प्रोसेस समझाने की जरूरत हो, वहाँ अपने आप Mermaid डायग्राम बनाओ।
4. Mermaid डायग्राम को हमेशा तीन बैकटिक के साथ लिखो। उदाहरण: mermaid कोड ब्लॉक में लिखो।
5. उदाहरण, टेबल और आसान भाषा का ज्यादा इस्तेमाल करो।
6. छात्र को प्रोत्साहित करो।
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
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
                max_tokens=1500
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"एरर: {str(e)}")

# ---------- Notes + Download ----------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 नोट्स बनाओ", use_container_width=True):
        if len(st.session_state.messages) >= 2:
            last_topic = st.session_state.messages[-2]["content"]
            with st.spinner("नोट्स तैयार हो रहे हैं..."):
                notes_prompt = f"छात्र {name} के लिए {student_class} {board} के {subject} विषय में '{last_topic}' के बहुत आसान और महत्वपूर्ण नोट्स बनाओ। पॉइंट्स में लिखो। जहाँ डायग्राम की जरूरत हो वहाँ Mermaid डायग्राम भी दो।"
                try:
                    notes_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": notes_prompt}],
                        temperature=0.5,
                        max_tokens=1500
                    )
                    notes = notes_response.choices[0].message.content
                    st.session_state.notes = notes
                    st.markdown("### 📝 आपके नोट्स")
                    st.markdown(notes)
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning("पहले कोई सवाल पूछो, फिर नोट्स बन सकते हैं।")

with col2:
    if "notes" in st.session_state:
        st.download_button(
            label="📄 नोट्स डाउनलोड करें",
            data=st.session_state.notes,
            file_name=f"GuruMind_Notes_{datetime.now().strftime('%d-%m-%Y')}.txt",
            mime="text/plain",
            use_container_width=True
        )
