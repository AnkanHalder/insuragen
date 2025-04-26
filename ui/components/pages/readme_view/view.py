import streamlit as st
from .readme_content import readme_text
class ReadMeView():
    @staticmethod
    def render():
        st.markdown(readme_text)