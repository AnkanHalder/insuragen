from typing import List
from langchain.embeddings import HuggingFaceEmbeddings


class EmbeddingManager:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.embedder = HuggingFaceEmbeddings(model_name=model_name)

    def embed_chunks(self, chunks: List[str]):
        return self.embedder.embed_documents(chunks)
    def get_model(self):
        return self.embedder