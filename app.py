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
temperature=0.6,
max_tokens=1500
)
reply = response.choices[0].message.content
st.markdown(reply)
st.session_state.messages.append({"role": "assistant", "content": reply})
except Exception as e:
st.error(f"एरर: {str(e)}")
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
if st.button("📝 नोट्स बनाओ", use_container_width=True):
if len(st.session_state.messages) >= 2:
last_topic = st.session_state.messages[-2]["content"]
with st.spinner("नोट्स तैयार हो रहे हैं..."):
notes_prompt = f"छात्र {name} के लिए {student_class} {board} {subject} में '{last_topic}' के आसान नोट्स बनाओ। पॉइंट्स में लिखो।"
try:
notes_response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
messages=[{"role": "user", "content": notes_prompt}],
temperature=0.5,
max_tokens=1200
)
notes = notes_response.choices[0].message.content
st.session_state.notes = notes
st.markdown("### 📝 आपके नोट्स")
st.markdown(notes)
except Exception as e:
st.error(str(e))
else:
st.warning("पहले कोई सवाल पूछो।")
with col2:
if "notes" in st.session_state:
st.download_button(
label="📄 नोट्स डाउनलोड करें",
data=st.session_state.notes,
file_name=f"GuruMind_Notes_{datetime.now().strftime('%d-%m-%Y')}.txt",
mime="text/plain",
use_container_width=True
)
