from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os, json, shutil
import constants.paths as base_paths
from core.services.pdf_service.doc_meta import DocMeta

class DeleteService:
    @staticmethod
    def delete(doc_key: str):
        # Step 1: Delete metadata
        doc_meta = DocMeta.get_meta(doc_key)
        if not doc_meta:
            print(f"No metadata found for key: {doc_key}")
            return False

        domain = doc_meta.get("domain")
        vector_store_path = os.path.join(base_paths.VECTOR_BASE_PATH, domain, "faiss_index")
        metadata_path = os.path.join(base_paths.VECTOR_BASE_PATH, domain, "chunks_metadata.json")

        # Step 2: Load and filter metadata
        if not os.path.exists(metadata_path):
            print(f"No metadata file found at {metadata_path}")
            return False

        with open(metadata_path, "r") as f:
            all_metadata = json.load(f)

        # Filter out chunks belonging to the deleted doc
        remaining_chunks = [meta for meta in all_metadata if not meta['metadata']["chunk_id"].startswith(doc_key)]

        if not remaining_chunks:
            # If no chunks remain, delete the FAISS index and metadata file entirely
            print("No remaining chunks. Removing entire domain vector store.")
            shutil.rmtree(os.path.join(base_paths.VECTOR_BASE_PATH, domain))
        else:
            # Step 3: Rebuild FAISS index from scratch using remaining chunks
            texts = []
            metadatas = []
            embeddings = HuggingFaceEmbeddings()
            for meta in remaining_chunks:
                texts.append(meta["text"])
                metadatas.append(meta)

            new_index = FAISS.from_texts(texts, embeddings, metadatas)
            new_index.save_local(vector_store_path)

            # Update chunk metadata
            with open(metadata_path, "w") as f:
                json.dump(remaining_chunks, f, indent=2)

        
        DocMeta.delete_meta(doc_key)
        print(f"✅ Deleted {doc_key} from domain '{domain}'")
        return True
