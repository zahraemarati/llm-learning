from pathlib import Path

from langchain_core.tools import tool
from pypdf import PdfReader


@tool
def pdf_reader(file_path: str) -> str:
    """
    Read text from a PDF file.

    Use this tool when the user asks to read or inspect
    the contents of a PDF document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The provided file must be a PDF.")

    reader = PdfReader(path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    if not pages:
        return "No readable text was found in the PDF."

    return "\n\n".join(pages)