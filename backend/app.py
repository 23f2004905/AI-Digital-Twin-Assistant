from fastapi import FastAPI, UploadFile, File
import os
import shutil
from pypdf import PdfReader

app = FastAPI(title="AI Digital Twin API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Backend Running 🚀"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return {
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:500]
    }