import ollama
from typing import List, Dict, Union
from string import Template
from core.services.ai.prompts.basic_template import DEFAULT_PROMPT_TEMPLATE

class QueryManager:
    def __init__(self, model_name="mistral", prompt_template: Template = DEFAULT_PROMPT_TEMPLATE):
        self.model_name = model_name
        self.prompt_template = prompt_template

    def format_chat_history(self, history: List[Dict[str, str]]) -> str:
        return "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in history])
    def format_chunks(self, chunks: List[Union[str, Dict]]) -> str:
        if not chunks:
            return "No relevant information was found."
        if isinstance(chunks[0], str):
            return "\n---\n".join(chunks)
        elif isinstance(chunks[0], dict):
            # 🔥 updated to use 'chunk' key instead of 'content'
            return "\n---\n".join([chunk.get("chunk", "") for chunk in chunks])
        else:
            raise ValueError("Unsupported chunk format.")

    def build_prompt(self, prompt: str, chunks: List, history: List[Dict[str, str]]) -> str:
        return self.prompt_template.substitute(
            chat_history=self.format_chat_history(history),
            chunks=self.format_chunks(chunks),
            question=prompt
        )

    def query_llm(self, prompt: str, chunks: List, history: List[Dict[str, str]]) -> str:
        final_prompt = self.build_prompt(prompt, chunks, history)
        print(final_prompt)
        stream = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": final_prompt}
            ],
            stream=True,
        )
        
        response = ""
        for chunk in stream:
            if 'message' in chunk:
                response += chunk["message"]["content"]
        return response
