import os
import pdfplumber
import docx

def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def _read_docx(path: str) -> str:
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs)

def _read_pdf(path: str) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)

def extract_text_from_path(path: str) -> str:
    ext = os.path.splitext(path.lower())[1]
    try:
        if ext == ".txt":
            return _read_txt(path)
        if ext == ".docx":
            return _read_docx(path)
        if ext == ".pdf":
            return _read_pdf(path)
        # For images, OCR is in utils/ocr.py (handled in app)
        return ""
    except Exception as e:
        return f"Text extraction failed: {e}"
