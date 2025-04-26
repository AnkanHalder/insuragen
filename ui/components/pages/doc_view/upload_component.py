import streamlit as st
from constants.domains import domains
from ui.models.session_state import StreamlitSessionState
from ui.constants.states import pipeline_state
from ui.controllers.upload_controller import UploadController  # Assuming you have this

st_session_state = StreamlitSessionState(pipeline_state)

class UploadComponent():
    @staticmethod
    def render():
        upload_in_progress = st_session_state.get_state('active') or False

        message_placeholder = st.empty()   

        def ping(info: str):
            message_placeholder.info(info)
            st_session_state.add_update_state('current-active_process',info)

        if not upload_in_progress:
            uploaded_file = st.file_uploader("Choose a file", type=["pdf"], disabled=upload_in_progress)
            user_domain = st.selectbox("Select Domain (This helps improve clarity)", domains, disabled=upload_in_progress)

            if uploaded_file:
                if st.button(f"Upload {uploaded_file.name}", disabled=upload_in_progress):
                    if user_domain.strip() != "":
                        ping(f'Initiating upload for: {uploaded_file.name}')  # Use placeholder
                        # Trigger the upload process in the controller
                        UploadController.upload(uploaded_file, user_domain, ping)
                    else:
                        message_placeholder.warning("Please select a domain before uploading.")  # Use placeholder
        else:
            ping("Upload in progress... Please wait.")  

        # Display success/error messages based on state (optional, can be handled in controller)
        upload_success = st_session_state.get_state('upload_success')
        upload_error = st_session_state.get_state('upload_error')

        if upload_success:
            message_placeholder.success(upload_success)
            st_session_state.delete_state('upload_success')
        if upload_error:
            message_placeholder.error(upload_error)
            st_session_state.delete_state('upload_error')
