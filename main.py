from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Doc Q&A API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    pdf_stream = io.BytesIO(contents)
    reader = PdfReader(pdf_stream)

    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() or ""

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "num_pages": len(reader.pages),
        "preview": extracted_text[:300]
    }