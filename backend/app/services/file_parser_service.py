from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_text_from_pdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def extract_text_from_docx(content: bytes) -> str:
    doc = Document(BytesIO(content))
    return "\n".join(paragraph.text for paragraph in doc.paragraphs).strip()


def extract_text(content: bytes, extension: str) -> str:
    extension = extension.lower()
    if extension == ".pdf":
        return extract_text_from_pdf(content)
    if extension == ".docx":
        return extract_text_from_docx(content)
    raise ValueError("Unsupported file extension")
