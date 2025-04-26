import streamlit as st
import time
from ui.models.session_state import StreamlitSessionState
from ui.controllers.query_controller import QueryController
from ui.constants.states import message_state

# Initialize message history
st_query_session = StreamlitSessionState(message_state)
if not st_query_session.state_exists(message_state):
    st_query_session.add_update_state(message_state, [])

# Session variables
st.session_state.setdefault("show_sources", False)
st.session_state.setdefault("pending_user_input", None)
st.session_state.setdefault("last_chunks", [])

class QNAView:
    @staticmethod
    def render():
        # Title and Clear Button
        st.title("🧠 Insurance Q&A Chat")
        if st.button("🧹 Clear Messages"):
            st_query_session.add_update_state(message_state, [])
            st.session_state.pending_user_input = None
            st.session_state.last_chunks = []
            st.session_state.show_sources = False
            st.rerun()

        # Chat history
        for msg in st_query_session.get_state(message_state):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # If assistant needs to respond
        if st.session_state.pending_user_input:
            QNAView._handle_assistant_response(st.session_state.pending_user_input)
            st.session_state.pending_user_input = None
            st.rerun()

        # Input box (👇 This is where we want the chunks to appear *after* this)
        user_input = st.chat_input("Ask your insurance question...")
        if user_input:
            history = st_query_session.get_state(message_state)
            history.append({"role": "user", "content": user_input})
            st_query_session.add_update_state(message_state, history)

            st.session_state.pending_user_input = user_input
            st.rerun()

        # Button to toggle chunk visibility
        if st.session_state.last_chunks:
            if st.button("🔎 Show Sources", key="toggle_sources"):
                st.session_state.show_sources = not st.session_state.show_sources

        # Retrieved Chunks (show below the input)
        if st.session_state.show_sources and st.session_state.last_chunks:
            st.markdown("### 📄 Retrieved Policies")
            for chunk in st.session_state.last_chunks:
                domain = chunk.get("domain", "Unknown")
                text = chunk.get("chunk", "")
                st.markdown(f"**{domain}**")
                st.code(text, language="")

    @staticmethod
    def _handle_assistant_response(prompt: str):
        history = st_query_session.get_state(message_state)

        # Insert temporary assistant message to show immediate feedback
        with st.chat_message("assistant"):
            temp_placeholder = st.empty()
            temp_placeholder.markdown("⏳ Thinking...")

        # Run query (simulate delay + real query)
        result = QueryController.query(prompt, history)
        st.session_state.last_chunks = result["chunks_used"]

        full_response = result["llm_response"]
        streamed_text = ""

        # Replace the temporary message with actual streamed response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            for word in full_response.split():
                streamed_text += word + " "
                placeholder.markdown(streamed_text + "|||")
            placeholder.markdown(streamed_text.strip())

        # Update message history with final response
        history.append({
            "role": "assistant",
            "content": streamed_text.strip()
        })
        st_query_session.add_update_state(message_state, history)