from pypdf import PdfWriter, PdfReader
from typing import BinaryIO
import io

def getPdfMetadata(file: BinaryIO):
    # Read the PDF file and extract metadata
    reader = PdfReader(file)
    return reader.metadata