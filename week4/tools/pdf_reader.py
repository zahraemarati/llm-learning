from langchain_core.tools import tool

from langchain_community.document_loaders import PyPDFLoader


@tool
def pdf_reader(file_path: str) -> str:
    """
    Read a PDF file and return its text content.

    Input:
    Path to a PDF file.

    Example:
    documents/paper.pdf
    """

    try:
        loader = PyPDFLoader(file_path)

        documents = loader.load()

        text = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        return text

    except Exception as e:
        return f"Error reading PDF: {str(e)}"