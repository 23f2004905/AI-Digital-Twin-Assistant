from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from utils.chunking import chunk_text
from database.chroma import add_chunks, search
from services.llm import ask_gemini
import os
import shutil
from pypdf import PdfReader


app = FastAPI(title="AI Digital Twin API")


class Question(BaseModel):
    question: str


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Backend Running 🚀"
    }


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

    chunks = chunk_text(text)
    add_chunks(chunks)

    return {
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:500]
    }


@app.post("/ask")
async def ask(question: Question):

    context = search(question.question)

    answer = ask_gemini(
        context=context,
        question=question.question
    )

    return {
        "question": question.question,
        "answer": answer
    }