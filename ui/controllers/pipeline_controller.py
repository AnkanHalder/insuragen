import streamlit as st
from ui.constants.states import meta_state
from core.services.pipeline.core_pipeline import Pipeline
from core.services.pdf_service.pdf_uploader import PDFUploader
from core.services.vector.vectorizer import Vectorizer
from ui.models.session_state import StreamlitSessionState

class PipelineController:
    def __init__(self, ping_fun=lambda *args, **kwargs: None):
        self.ping = ping_fun
        self.st_session_state_meta = StreamlitSessionState(meta_state)

    def run_pipeline(self, file, filename, size, domain=None):
        """
        Runs the pipeline with the given file, filename, size, and domain.
        """
        try:
            self.ping("🔁 Starting Pipeline...")
            uploaded_file, meta = PDFUploader(file, filename, size, domain, ping_fun=self.ping).run()
            self.ping("✅ Beginning Vectorizer")
            Vectorizer(domain,ping_fun= self.ping).run(uploaded_file=uploaded_file, filename=meta['filename'] , doc_meta=meta )
            self.ping("✅ Pipeline completed!")
            self.ping("Pipeline completed successfully!")

        except Exception as e:
            print(e,str(e))
            self.ping("❌ Pipeline failed.")
            st.error(f"An error occurred during the pipeline: {e}")
        finally:
            self.st_session_state_meta.add_update_state('active', False)
            self.st_session_state_meta.delete_state('current-active-process')
