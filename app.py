import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="GuruMind AI", page_icon="🎓", layout="wide")

# --- Sidebar (Guru Sir) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=180)
    st.markdown("### 👨‍🏫 Guru Sir")
    st.markdown("आपका व्यक्तिगत शिक्षक")
    st.markdown("---")
    
    name = st.text_input("आपका नाम", value="Navneet")
    student_class = st.selectbox("कक्षा", ["11वीं", "12वीं"])
    board = st.selectbox("बोर्ड", ["UP Board", "CBSE", "ICSE", "अन्य"])
    
    st.markdown("---")
    st.info(f"नमस्ते **{name}**!\nमैं आपकी **{student_class}** की पढ़ाई में मदद करूँगा।")

# --- Main Area ---
st.title("🎓 GuruMind AI")
st.caption("Guru Sir के साथ पढ़ाई करो")

api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("API Key नहीं मिली। Settings → Secrets में जोड़ें।")
    st.stop()

client = Groq(api_key=api_key)

SYSTEM_PROMPT = f"""तुम Guru Sir हो — बहुत स्मार्ट, धैर्यवान और दोस्ताना शिक्षक।
छात्र का नाम: {name}
कक्षा: {student_class}
बोर्ड: {board}

हमेशा आसान हिंदी + थोड़ी अंग्रेजी (Hinglish) में बात करो।
हर जवाब के बाद पूछो: "समझ आया क्या? या मैं इसे किसी और तरीके से समझाऊँ?"
उदाहरण देकर बहुत आसान भाषा में समझाओ।
छात्र को प्रोत्साहित करो।"""

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
                max_tokens=1200
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"एरर: {str(e)}")

# Notes button
st.markdown("---")
if st.button("📝 इस टॉपिक के नोट्स बनाओ"):
    if st.session_state.messages:
        last_topic = st.session_state.messages[-2]["content"] if len(st.session_state.messages) >= 2 else "सामान्य"
        with st.spinner("नोट्स बन रहे हैं..."):
            notes_prompt = f"छात्र {name} के लिए {student_class} {board} के अनुसार '{last_topic}' विषय के बहुत आसान और महत्वपूर्ण नोट्स बनाओ। पॉइंट्स में लिखो।"
            try:
                notes_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": notes_prompt}],
                    temperature=0.5,
                    max_tokens=1000
                )
                st.markdown("### 📝 नोट्स")
                st.markdown(notes_response.choices[0].message.content)
            except Exception as e:
                st.error(str(e))
    else:
        st.warning("पहले कोई सवाल पूछो, फिर नोट्स बन सकते हैं।")
