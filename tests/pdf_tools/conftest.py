# tests/tools/pdf_tools/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_pdf_bytes():
    return (Path(__file__).parent / "fixtures" / "sample-pdf-a4-size-65kb.pdf").read_bytes()

@pytest.fixture
def password_protected_pdf_bytes():
    return (Path(__file__).parent / "fixtures" / "protected.pdf").read_bytes()