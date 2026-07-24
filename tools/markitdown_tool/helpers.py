import io
from pathlib import Path
from typing import BinaryIO

allowed_extensions = {".pdf", ".docx"}
allowed_mimetypes = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
max_size_bytes = 10 * 1024 * 1024

def validateInputFileType(filename: str, content_type: str | None = None) -> bool:
    """
    Validate the input file based on its extension and content type.
    Returns True if the file is valid, False otherwise.
    """
    # Get the file extension
    extension = Path(filename).suffix.lower()

    # Check if the extension and content type are allowed
    if extension in allowed_extensions and (content_type is None or content_type in allowed_mimetypes):
        return True
    return False

def validateInputFileSize(file: BinaryIO) -> bool:
    """
    Validate the input file size.
    Returns True if the file size is within the limit, False otherwise.
    """
    # Move the cursor to the end of the file to get its size
    file.seek(0, io.SEEK_END)
    size_in_bytes = file.tell()
    
    # Move the cursor back to the beginning of the file
    file.seek(0)

    return size_in_bytes <= max_size_bytes