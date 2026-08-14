from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Doc Q&A API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents)
    }