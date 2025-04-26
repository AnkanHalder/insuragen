import streamlit as st
from ui.constants import strings as strgs
from ui.components.pages.doc_view.doc_cards import DocComponentUI
from ui.models.session_state import StreamlitSessionState
from ui.components.pages.doc_view.upload_component import UploadComponent
from core.services.pdf_service.doc_meta import DocMeta
from constants.domains import domains

class DocViewUI:
    @staticmethod
    def render():
        st.title(strgs.title)
        st.markdown(strgs.description)
        st.subheader("Upload Section")
        UploadComponent.render()
        st_session_state = StreamlitSessionState('doc_metas')
        st_session_state.add_update_state("list", DocMeta._load_all_meta())
        
        st.subheader(strgs.uploaded_docs)
        doc_meta_array = st_session_state.get_state("list") or []
        for doc_meta in doc_meta_array:
            DocComponentUI.render(doc_meta)
