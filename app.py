from pdf_utils import extract_text_from_pdf

import streamlit as st
from ai_engine import get_ai_response
from database import init_db, save_message, load_messages
import sqlite3

if "username" not in st.session_state:
    st.session_state.username = None


st.set_page_config(page_title="Study Assistant")
st.title("🤖 AI Study Assistant")
st.markdown("""
<style>

/* Page background */
.stApp {
    background-color: #0e1117;
}

/* Input box */
.stTextInput input {
    background-color: #1c1f26;
    color: white;
    border-radius: 10px;
}

/* Chat container */
.chat-box {
    max-height: 450px;
    overflow-y: auto;
    padding: 10px;
}

/* User message */
.user {
    background-color: #2d8cff;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    width: fit-content;
    max-width: 70%;
    align-self: flex-end;
}

/* AI message */
.ai {
    background-color: #3a3f4b;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px;
    width: fit-content;
    max-width: 70%;
    align-self: flex-start;
}

</style>
""", unsafe_allow_html=True)

if st.session_state.username is None:
    st.subheader("👤 Enter your name to start")
    name = st.text_input("Your name")

    if st.button("Start"):
        st.session_state.username = name
        st.rerun()

    st.stop()

st.subheader("📄 Upload Previous Year Question Papers")

uploaded_files = st.file_uploader(
    "Upload 2 or more question papers (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# If user has uploaded at least 2 PDFs
if uploaded_files and len(uploaded_files) >= 2:

    all_text = ""

    # Read every PDF and extract its text
    for file in uploaded_files:
        all_text += extract_text_from_pdf(file)

    # Button to start analysis
    if st.button("🔍 Analyze Question Papers"):
        with st.spinner("Analyzing important questions..."):

            # Send all text to Gemini
            prompt = (
                "You are an exam expert. Analyze the following previous year question papers. "
                "Find the questions that appear more than once and list the important repeated questions.\n\n"
                + all_text
            )

            result = get_ai_response(prompt)

            st.subheader("📌 Important Repeated Questions")
            st.write(result)


st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
}

.user-msg {
    background-color: #2b2b2b;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 6px;
    max-width: 70%;
    align-self: flex-end;
}

.ai-msg {
    background-color: #1f3c88;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 6px;
    max-width: 70%;
    align-self: flex-start;
}
</style>
""", unsafe_allow_html=True)

# Create a placeholder for the Clear Chat button
clear_placeholder = st.empty()

with clear_placeholder:
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = []

        conn = sqlite3.connect("chat_history.db")
        conn.execute("DELETE FROM chats")
        conn.commit()
        conn.close()

        st.rerun()




# Create database if it does not exist
init_db()


if "messages" not in st.session_state:
    st.session_state.messages = []

    # Load messages from database
    db_messages = load_messages(st.session_state.username)

    for role, msg in db_messages:
        st.session_state.messages.append({"role": role, "content": msg})



# Clear chat button
#if st.button("🗑️ Clear Chat", key="clear_chat"):

  #  st.session_state["messages"] = []
  #  st.rerun()



# Display old messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)



# Input box
user_input = st.text_input("Ask me anything:", key="q")


if user_input and st.session_state.get("last_input") != user_input:
    # Save user message
    
    st.session_state["last_input"] = user_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_message("user", user_input)

    # Get AI response
    ai_reply = get_ai_response(user_input)

    # Save AI message
    st.session_state.messages.append({"role": "ai", "content": ai_reply})
    save_message("ai", ai_reply)

    st.rerun()

if st.button("🗑️ Clear Chat"):
   st.session_state.messages = []

   import sqlite3
   conn = sqlite3.connect("chat_history.db")
   conn.execute("DELETE FROM chats")
   conn.commit()
   conn.close()

   st.rerun()

  
