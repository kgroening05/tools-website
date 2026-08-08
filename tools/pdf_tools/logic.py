from pypdf import PdfWriter, PdfReader
from pypdf.errors import PdfReadError
import io
from pathlib import Path

KEYWORDS_START = {"begin", "start", "first"}
KEYWORDS_END = {"end", "last"}
KEYWORDS_REST = {"remaining", "rest"}

def load_pdf(data: bytes) -> PdfReader | str:
    try:
        reader = PdfReader(io.BytesIO(data))
    except PdfReadError as e:
        return f"Could not read PDF: {e}"
    except Exception as e:
        return f"Unexpected error reading PDF: {e}"

    if reader.is_encrypted:
        # Try empty password — some PDFs are technically encrypted but with no protection
        try:
            if not reader.decrypt(""):
                return "PDF is password-protected"
        except Exception:
            return "PDF is password-protected"

    if len(reader.pages) == 0:
        return "PDF contains no pages"

    return reader

def get_page_count(reader: PdfReader) -> int:
    # Note: this is a trivial accessor, but it exists to abstract the pypdf internals.
    return len(reader.pages)

def split_pdf(reader: PdfReader, start: int, end: int) -> bytes:
    """Extract pages start..end (1-indexed, inclusive) as PDF bytes."""
    writer = PdfWriter()
    for page_num in range(start - 1, end):   # convert to 0-indexed for pypdf
        writer.add_page(reader.pages[page_num])
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()

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


def _resolve_endpoint(token: str, total_pages: int, last_end: int, is_start: bool) -> int | str:
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

def _render_error(request, ranges):
    pass

def save_pdf(pdf_data: bytes, filename: str, output: Path, job_id: str) -> None:
    full_path = output / job_id / filename
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(pdf_data)