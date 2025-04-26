import streamlit as st
from ui.components.sidebar import sidebar
from ui.constants.pages import PAGES
from ui.components.pages.doc_view.doc_view_ui import DocViewUI
from ui.components.pages.qna_view.view import QNAView
from ui.components.pages.readme_view.view import ReadMeView
from ui.models.session_state import StreamlitSessionState
from ui.constants.states import pipeline_state

if pipeline_state not in st.session_state:
    st.session_state[pipeline_state] = {'active': False}
    st.write(f"Initialized {pipeline_state}: {st.session_state[pipeline_state]}")

def show_readme():
    ReadMeView.render()

def show_upload():
    DocViewUI.render()

def show_query():
    QNAView.render()

sidebar()
if(st.session_state.page == PAGES["Query"]):
    show_query()
elif(st.session_state.page == PAGES["Upload"]):
    show_upload()
else:
    show_readme()



