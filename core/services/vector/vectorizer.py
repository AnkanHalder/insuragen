from .chunk_service import ChunkerModel
from .embedding_manager import EmbeddingManager
from .vectors import DomainVectorStore
from core.services.pipeline.process import Process
class Vectorizer(Process):
    def __init__(self, domain: str, ping_fun= lambda: None):
        self.domain = domain
        self.chunker = ChunkerModel()
        self.embed_manager = EmbeddingManager()
        self.vector_store = DomainVectorStore(domain)
        self.ping = ping_fun
    def run(self, uploaded_file, filename, doc_meta):
        self.ping(f"File Received: {filename}. Beginning Chunking")
        chunks, num_pages = self.chunker.get_chunks(uploaded_file)
        print("Chunking successfull. Starting Embeddings")
        self.ping("Chunking successfull. Starting Embeddings")
        embeddings = self.embed_manager.embed_chunks(chunks)
        print("Created Embeddings . Saving ...........")
        self.ping("Created Embeddings . Saving ...........")
        self.vector_store.update_store(chunks, embeddings,  doc_meta)
        print(f"Saved. Doc Metadata: { doc_meta}")
        self.ping(f"Saved. Doc Metadata: { doc_meta}")
        print(f"Successfully processed and updated domain '{self.domain}' with document '{filename}'.")
        self.ping(f"Successfully processed and updated domain '{self.domain}' with document '{filename}'.")
        return doc_meta

