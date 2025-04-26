import streamlit as st
from ui.models.session_state import StreamlitSessionState
from ui.constants.states import pipeline_state
from .pipeline_controller import PipelineController
import time


class UploadController():
    @staticmethod
    def upload(raw_file,domain: str, ping_fun = lambda: None):
        st_session_state = StreamlitSessionState(pipeline_state)
        if st_session_state.state_exists('active') and st_session_state.get_state('active') == True:
            st.error("Upload Pipeline is currently Active. Please Wait before trying Again")
        else:
            st_session_state.add_update_state('active',True)
            if not st_session_state.state_exists('current-active_process'):
                st_session_state.add_update_state('current-active_process','Running.... Please Wait')
            with st.spinner(st_session_state.get_state('current-active_process')):
                time.sleep(1)
                PipelineController(ping_fun=ping_fun).run_pipeline(file=raw_file,filename=raw_file.name,size=raw_file.size, domain=domain)
                st_session_state.add_update_state('active', False)
                st_session_state.add_update_state('upload_success', "✅ Upload and processing completed.")


            st_session_state.add_update_state('active',False)
            

            