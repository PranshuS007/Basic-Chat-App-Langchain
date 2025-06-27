import streamlit as st
import requests
from chat_engine import conversation, memory


st.title("Chatbot")
st.markdown("Ask me anything!!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("🔌 End Conversation"):
    st.session_state.chat_history = []
    # memory.clear()
    # st.success("Conversation ended")

user_input = st.chat_input("Type your message.......")

if user_input:
    try:
        res = requests.post("http://fastapi-service:8000/chat", json={"query": user_input})
        response = res.json()["response"]
        st.session_state.chat_history.append(("You",user_input))
        st.session_state.chat_history.append(("Bot",response))
    except Exception as e:
        st.error(f"Error talking to chatbot: {e}")

for speaker, msg in st.session_state.chat_history:
    with st.chat_message(speaker):
        st.markdown(msg)