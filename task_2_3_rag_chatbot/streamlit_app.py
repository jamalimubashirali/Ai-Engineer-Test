"""
streamlit_app.py — A simple Streamlit frontend for the RAG Knowledge Bot.

Run with:
    streamlit run streamlit_app.py
"""
import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from services import build_retriever, build_rag_chain, query as rag_query
from config import Env

# ------------------------------------------------------------------ #
#  Page Config & Styles                                              #
# ------------------------------------------------------------------ #
st.set_page_config(page_title="Agency Knowledge Bot", page_icon="🤖")

st.title("🤖 Agency Campaign Knowledge Bot")
st.markdown(
    "Ask me about our **agency case studies** or **brand guidelines**. "
    "I'll answer strictly from our verified document base."
)

# ------------------------------------------------------------------ #
#  Initialize Backend (Cached)                                       #
# ------------------------------------------------------------------ #
@st.cache_resource
def get_rag_chain():
    """Build the retriever and chain once, and cache it for the session."""
    try:
        # Validate Env before heavy loading
        Env.validate()
        retriever = build_retriever(docs_dir="documents")
        chain = build_rag_chain(retriever)
        return chain
    except Exception as e:
        st.error(f"Failed to initialize RAG: {e}")
        return None

chain = get_rag_chain()

# ------------------------------------------------------------------ #
#  Session State for Chat History                                    #
# ------------------------------------------------------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source" in message and message["source"] != "N/A":
            st.caption(f"**Source:** {message['source']}")
        if "quote" in message and message["quote"]:
            st.info(f"*{message['quote']}*")

# ------------------------------------------------------------------ #
#  Chat Input & Query Logic                                          #
# ------------------------------------------------------------------ #
if chain is None:
    st.warning("Please check your `.env` configuration or document folder.")
else:
    if prompt := st.chat_input("Ask a question about our case studies..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate bot response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                answer = rag_query(chain, prompt)
            
            st.markdown(answer.answer)
            if answer.source and answer.source != "N/A" and answer.source != "Unknown":
                st.caption(f"**Source:** {answer.source}")
            if answer.quote:
                st.info(f"*{answer.quote}*")
            
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer.answer,
            "source": answer.source,
            "quote": answer.quote
        })
