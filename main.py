from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import io
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def get_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


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

    chunks = chunk_text(extracted_text)

    embeddings = [get_embedding(chunk) for chunk in chunks]

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "num_pages": len(reader.pages),
        "num_chunks": len(chunks),
        "num_embeddings": len(embeddings),
        "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
        "first_embedding_preview": embeddings[0][:5] if embeddings else None
    }