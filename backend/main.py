# backend/main.py
import os
import tempfile

import nltk
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.rag.answering_engine import (
    add_document,
    check_document_exists,
    delete_document,
    get_answer,
)

load_dotenv(find_dotenv())


class QuestionModel(BaseModel):
    document_id: str
    question: str


class DocumentModel(BaseModel):
    document_id: str


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

origins = [os.environ.get("CLIENT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# download tokenizer modules
nltk.download("punkt")
nltk.download("punkt_tab")


@app.post("/api/answer_question")
async def answer_question(req: QuestionModel):
    return {"answer": get_answer(req.question, req.document_id)}


@app.post("/api/upload_document")
async def upload_document(file: UploadFile):
    with tempfile.NamedTemporaryFile(suffix=file.filename) as tmp:
        tmp.write(file.file.read())
        return {"document_id": add_document(tmp.name)}


@app.get("/api/test")
async def test():
    return {"response": "This test fail succesfully"}


@app.get("/api/check_document")
async def check_document(document_id: str):
    try:
        exists = check_document_exists(document_id)
        return {"exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/delete_document")
async def remove_document(req: DocumentModel):
    try:
        delete_document(req.document_id)
        return {"message": "Document deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
