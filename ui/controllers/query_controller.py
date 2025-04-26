from core.services.vector.retriver import Retriever
from core.services.reranker.reranker_service import Reranker
from core.services.ai.query.query_manager import QueryManager

reranker = Reranker()

class QueryController():
    @staticmethod
    def query(prompt: str, history: list = []):  
        chunks = Retriever.retrieve(prompt)
        reranked_chunks = reranker.rerank(prompt, chunks)

        answer = QueryManager().query_llm(prompt, reranked_chunks, history) 
        return {
            "llm_response": answer,
            "chunks_used": reranked_chunks
        }
