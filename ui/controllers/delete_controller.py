from core.services.cleanup.delete_service import DeleteService
import  streamlit as st
class DeleteController():
    @staticmethod
    def delete(doc_key : str):
        DeleteService.delete(doc_key=doc_key)
