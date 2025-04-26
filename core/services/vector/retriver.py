from typing import List, Dict
import os, json
from constants.domains import domains
from constants.paths import VECTOR_BASE_PATH
from langchain_community.vectorstores import FAISS
from core.services.vector.embedding_manager import EmbeddingManager

class Retriever:
    @staticmethod
    def retrieve(query: str) -> List[Dict[str, str]]:
        with open("constants/settings.json", "r") as f:
            settings = json.load(f)

        chunks_per_domain = settings.get("chunk_each_domain", 5)
        embeddings = EmbeddingManager().get_model()

        results = []

        for domain in domains:
            domain_path = os.path.join(VECTOR_BASE_PATH, domain, "faiss_index")
            if not os.path.exists(domain_path):
                continue

            try:
                vector_store = FAISS.load_local(domain_path, embeddings, allow_dangerous_deserialization=True)
                docs = vector_store.similarity_search(query, k=chunks_per_domain)
                for doc in docs:
                    results.append({
                        "domain": domain,
                        "chunk": doc.page_content
                    })
            except Exception as e:
                print(f"Error retrieving from domain {domain}: {e}")
                continue

        return results
