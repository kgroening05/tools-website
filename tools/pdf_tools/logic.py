from pypdf import PdfWriter, PdfReader
from typing import BinaryIO
import io

def getPdfMetadata(file: BinaryIO):
    # Read the PDF file and extract metadata
    reader = PdfReader(file)
    return reader.metadata

def splitPdf(file: BinaryIO, start_page: int, end_page: int)->io.BytesIO:
    reader = PdfReader(file)
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    output = io.BytesIO()
    writer.write(output)
    return output

KEYWORDS_START = {"begin", "start", "first"}
KEYWORDS_END = {"end", "last"}
KEYWORDS_REST = {"remaining", "rest"}

def parse_range_spec(spec: str, total_pages: int) -> list[tuple[int, int]] | str:
    if not spec.strip():
        return "Range spec is empty"

    spec = spec.replace(";", ",").lower()
    result = []
    last_end = 0

    for raw in spec.split(","):
        piece = raw.strip()
        if not piece:
            return "Empty range in spec"

        # Whole-piece keyword (remaining/rest)
        if piece in KEYWORDS_REST:
            if last_end >= total_pages:
                return "'remaining' has no pages left"
            result.append((last_end + 1, total_pages))
            last_end = total_pages
            continue

        # Single page or range
        if "-" in piece:
            parts = piece.split("-")
            parts = [piece.strip() for piece in parts]
            if len(parts) != 2 or not parts[0] or not parts[1]:
                return f"Invalid range: {piece}"
            start = _resolve_endpoint(parts[0], total_pages, last_end, is_start=True)
            end = _resolve_endpoint(parts[1], total_pages, last_end, is_start=False)
        else:
            start = end = _resolve_endpoint(piece, total_pages, last_end, is_start=True)

        # Any endpoint resolution failure surfaces as a string
        if isinstance(start, str):
            return start
        if isinstance(end, str):
            return end

        if start < 1:
            return f"Page {start} is invalid — pages start at 1"
        if end > total_pages:
            return f"Page {end} exceeds the document's {total_pages} pages"
        if start > end:
            return f"Range {piece} is reversed (start > end)"

        result.append((start, end))
        last_end = end

    return result


def _resolve_endpoint(
    token: str, total_pages: int, last_end: int, is_start: bool
) -> int | str:
    """Resolve a single endpoint (a number or a keyword). Returns int or error string."""
    if token in KEYWORDS_START:
        return 1
    if token in KEYWORDS_END:
        return total_pages
    if token in KEYWORDS_REST:
        # "remaining" only valid as a whole piece, not an endpoint
        return f"'{token}' can only be used on its own, not inside a range"
    if token.lstrip("-").isnumeric():
        # Reject negatives explicitly — isnumeric() alone rejects them (no minus sign)
        # but let's be defensive.
        n = int(token)
        if n < 1:
            return f"Page {n} is invalid — pages start at 1"
        return n
    return f"Unknown token: '{token}'"