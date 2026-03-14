"""
Utility functions — PDF text extraction and helpers.
"""

import io
import PyPDF2


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from an uploaded PDF file.
    Returns concatenated text from all pages.
    """
    pdf_bytes = uploaded_file.read()
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"\n--- Page {page_num + 1} ---\n{page_text}"

    if not text.strip():
        raise ValueError(
            "Could not extract text from this PDF. "
            "It may be a scanned image PDF. Please use a text-based PDF."
        )

    return text


def truncate_text(text: str, max_chars: int = 10000) -> str:
    """Truncate text to avoid exceeding LLM context limits."""
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated for context limit]"
    return text
