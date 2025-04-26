import streamlit as st
from ui.constants.pages import PAGES

# Sidebar for navigation
def sidebar():
    with st.sidebar:
        st.title("📚 Navigation")
        selected_page = st.radio("Go to", list(PAGES.keys()))
        st.session_state.page = PAGES[selected_page]


