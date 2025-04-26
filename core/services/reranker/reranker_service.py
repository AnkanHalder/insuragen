import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Dict

class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", threshold: float = 0.5):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()
        self.threshold = threshold  # Minimum average score required

    def rerank(self, query: str, chunk_items: List[Dict[str, str]], top_k: int = 5) -> List[Dict[str, str]]:
        if not chunk_items:
            return []

        chunks = [item["chunk"] for item in chunk_items]

        inputs = self.tokenizer(
            [query] * len(chunks),
            chunks,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits.squeeze(-1)  # Shape: (num_chunks,)

        # Select top-k indices
        top_k = min(top_k, len(chunks))
        top_values, top_indices = torch.topk(logits, k=top_k)

        avg_score = top_values.mean().item()

        # 🚨 Check against threshold
        if avg_score < self.threshold:
            return []

        # Otherwise return top-k reranked chunks
        reranked = [chunk_items[i] for i in top_indices.tolist()]
        return reranked
