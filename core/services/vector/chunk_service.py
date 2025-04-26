from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChunkerModel():
    def __init__(self,model = None, chunk_size=500, chunk_overlap=50):
        self.model = model if model else RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    def get_chunks(self,pdf_doc):
        full_text = ""
        for page in pdf_doc:
            full_text += page.get_text()
        chunks = self.model.split_text(full_text)
        return chunks, len(pdf_doc) 
