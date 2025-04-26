import streamlit as st
from ui.controllers.delete_controller import DeleteController

from ui.controllers.delete_controller import DeleteController
from ui.models.session_state import StreamlitSessionState

st_session_state = StreamlitSessionState('doc_metas')

class DocComponentUI:
    @staticmethod
    def render(doc_meta):
        doc_key = doc_meta["key"]
        

        with st.container():
            st.markdown("---") 
            col1, col2 = st.columns([3, 2])
            with col1:
                for key in doc_meta:
                    if key != "key":
                        st.markdown(f"**{key}:** {doc_meta[key]}")
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{doc_key}"):
                    DeleteController.delete(doc_key)
                    
                    # Update session state: remove from 'list'
                    all_docs = st_session_state.get_state("list") or []
                    updated_docs = [doc for doc in all_docs if doc.get("key") != doc_key]
                    st_session_state.add_update_state("list", updated_docs)
                    
                    st.rerun()
