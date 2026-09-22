import pytest

from tools.pdf_reader import pdf_reader


def test_pdf_reader_file_not_found():
    with pytest.raises(FileNotFoundError):
        pdf_reader.invoke(
            {
                "file_path": "missing.pdf",
            }
        )
    