import fitz
import os
import datetime
import uuid
from core.services.pdf_service.doc_meta import DocMeta
from core.services.pipeline.process import Process  

class PDFUploader(Process):
    def __init__(self, file, filename: str, size: int, domain: str = None, ping_fun = lambda: None):
        self.file = file
        self.filename = filename
        self.size =  size / (1024 * 1024)
        self.domain = domain or "Uncategorized"
        self.upload_date = datetime.datetime.now().isoformat()
        self.doc = None
        self.text = None
        self.doc_key = str(uuid.uuid4()) + f"_{os.path.splitext(filename)[0]}"
        self.ping = ping_fun
        self.metadata = {}

    def get_read_file(self):
        """Open the uploaded file using PyMuPDF."""
        self.ping("Reading File ......")
        try:
            self.doc = fitz.open(stream=self.file.read(), filetype="pdf")
            return self.doc
        except Exception as e:
            raise RuntimeError(f"Error opening PDF: {e}")

    def plain_text(self):
        """Extract plain text from the PDF document."""
        if self.doc is None:
            self.get_read_file()

        extracted_text = ""
        for page in self.doc:
            extracted_text += page.get_text()

        self.text = extracted_text
        return self.text

    def save_meta(self):
        """Save metadata using DocMeta class."""
        self.ping("Saving Meta")
        self.metadata = {
            "key" : self.doc_key,
            "filename": self.filename,
            "size_bytes": self.size,
            "upload_date": self.upload_date,
            "num_pages": len(self.doc) if self.doc else 0,
            "domain": self.domain,
        }
        DocMeta.add_update_meta(self.doc_key, self.metadata)
        print('HELLO')
        return self.metadata

    def run(self):
        file = self.get_read_file()
        meta = self.save_meta()
        print(f"[PDFUploader] Processed and saved metadata for: {meta['key']}")
        return (file,meta)
