import json
import os
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from core.services.vector.embedding_manager import EmbeddingManager

class DomainVectorStore:
    """
    Manages a FAISS vector index scoped by domain.
    Stores vectors and metadata per domain in a structured folder.
    """

    def __init__(self, domain: str, base_path: str = "data"):
        self.domain = domain
        self.index_path = os.path.join(base_path, domain)
        os.makedirs(self.index_path, exist_ok=True)

        self.faiss_path = os.path.join(self.index_path, "faiss_index")
        self.chunk_metadata_path = os.path.join(self.index_path, "chunks_metadata.json")
        self.embedding_model = EmbeddingManager().get_model()

        if os.path.exists(self.faiss_path):
            self.vector_store = FAISS.load_local(
                self.faiss_path,
                self.embedding_model,
                allow_dangerous_deserialization=True  # Ideally avoid this if possible
            )
        else:
            self.vector_store = None

    def update_store(self, chunks: List[str], embeddings: List[List[float]], doc_metadata: Dict):
        """
        Updates or creates the vector store with new chunks and their embeddings.
        Also updates chunk-level metadata.
        """
        if not chunks or not embeddings or len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings must be non-empty and of equal length.")

        # Build metadata for chunks
        chunk_metadata = [{"chunk_id": f"{doc_metadata['key']}_chunk_{i}"} for i in range(len(chunks))]

        # Create or merge FAISS vector store
        new_store = FAISS.from_embeddings(zip(chunks, embeddings), self.embedding_model)

        if self.vector_store is None:
            self.vector_store = new_store
        else:
            self.vector_store.merge_from(new_store)

        self.vector_store.save_local(self.faiss_path)

        # Load existing metadata (if present)
        if os.path.exists(self.chunk_metadata_path):
            with open(self.chunk_metadata_path, "r", encoding="utf-8") as f:
                existing_metadata = json.load(f)
        else:
            existing_metadata = []

        # Append new metadata
        new_metadata = [{"text": text, "metadata": meta} for text, meta in zip(chunks, chunk_metadata)]
        existing_metadata.extend(new_metadata)

        # Save updated metadata
        with open(self.chunk_metadata_path, "w", encoding="utf-8") as f:
            json.dump(existing_metadata, f, indent=2)
