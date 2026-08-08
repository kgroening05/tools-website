from pypdf import PdfReader
from tools.pdf_tools.logic import load_pdf


def test_load_pdf_valid_returns_reader(sample_pdf_bytes):
    result = load_pdf(sample_pdf_bytes)
    assert isinstance(result, PdfReader), f"expected PdfReader, got {result!r}"


def test_load_pdf_garbage_returns_error_message():
    result = load_pdf(b"not a pdf at all")
    assert isinstance(result, str)
    assert result, "error message should not be empty"


def test_load_pdf_empty_returns_error_message():
    result = load_pdf(b"")
    assert isinstance(result, str)
    assert result


def test_load_pdf_password_protected_returns_password_error(password_protected_pdf_bytes):
    result = load_pdf(password_protected_pdf_bytes)
    assert isinstance(result, str)
    assert "password" in result.lower() or "encrypt" in result.lower(), (
        f"error should mention password/encryption, got: {result!r}"
    )