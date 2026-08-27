from fastapi import FastAPI, UploadFile, File
import fitz
from PyPDF2 import PdfReader
import uuid
import os
import re

app = FastAPI()

papers = {}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\x0c", "\n")
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_title(text: str) -> str:
    if not text:
        return "Title not found"

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if len(line.split()) < 3:
            continue
        if line.lower().startswith(("abstract", "introduction", "conclusion", "references")):
            continue
        if 20 <= len(line) <= 140:
            return line

    first_sentence = re.split(r"(?<=[.!?])\s+", text)[0]
    return first_sentence[:120].strip() or "Title not found"


def generate_summary(text: str) -> str:
    cleaned = normalize_text(text)
    if not cleaned:
        return "No meaningful content found."

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    sentences = [s.strip() for s in sentences if len(s.split()) >= 8]

    if not sentences:
        return "No meaningful content found."

    selected = sentences[:5]
    return " ".join(selected)


def extract_text(pdf_path):
    text_parts = []

    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            page_text = page.get_text("text")
            if page_text and page_text.strip():
                text_parts.append(page_text.strip())
        doc.close()
    except Exception:
        text_parts = []

    if not text_parts:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                if page_text and page_text.strip():
                    text_parts.append(page_text.strip())
        except Exception:
            text_parts = []

    if not text_parts:
        return ""

    return normalize_text("\n\n".join(text_parts))


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    paper_id = str(uuid.uuid4())
    path = f"{paper_id}.pdf"

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)
    papers[paper_id] = text

    if os.path.exists(path):
        os.remove(path)

    return {"paper_id": paper_id}


@app.post("/summarize")
def summarize(paper_id: str):
    text = papers.get(paper_id, "")

    if not text.strip():
        return {"summary": "No text extracted from PDF"}

    summary = generate_summary(text)
    return {"summary": summary}


@app.post("/ask")
def ask(paper_id: str, question: str):
    text = papers.get(paper_id, "")

    if not text.strip():
        return {"answer": "No paper found"}

    q = question.strip().lower()
    if not q:
        return {"answer": "Please ask a question about the paper"}

    if "title" in q:
        return {"answer": extract_title(text)}

    cleaned_text = normalize_text(text)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)

    for sentence in sentences:
        if q in sentence.lower():
            return {"answer": sentence.strip()}

    q_words = [word for word in re.findall(r"[a-zA-Z]{3,}", q) if len(word) > 2]
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in q_words):
            return {"answer": sentence.strip()}

    return {"answer": "Answer not found in the paper"}