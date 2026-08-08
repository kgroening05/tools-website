from fastapi import APIRouter, Request, UploadFile, File, Form
from pathlib import Path
import template_env
from .logic import load_pdf, split_pdf, parse_range_spec, get_page_count, _render_error, save_pdf
import secrets

router = APIRouter()
OUTPUT_DIR = template_env.OUTPUT_DIR
    
@router.get("/")
def page(request: Request):
    return template_env.templates.TemplateResponse(
        request=request,
        name="pdf_tools_page.html",
        context={},
    )

@router.post("/split")
async def split(request: Request, file: UploadFile = File(...), range_spec: str = Form(...)):
    data = await file.read()

    reader = load_pdf(data)
    if isinstance(reader, str):
        return _render_error(request, reader)

    page_count = get_page_count(reader)

    ranges = parse_range_spec(range_spec, page_count)
    if isinstance(ranges, str):
        return _render_error(request, ranges)

    outputs = []
    base = Path(file.filename or "document").stem
    job_id = secrets.token_urlsafe(16)
    for start, end in ranges:
        pdf_bytes = split_pdf(reader, start, end)
        filename = f"{base}-p{start}-{end}.pdf"
        save_pdf(pdf_bytes, filename, OUTPUT_DIR, job_id)
        outputs.append({
            "filename": filename,
            "url": f"/output/{job_id}/{filename}",
        })

    # Save outputs, render result page with download links
    return template_env.templates.TemplateResponse(
        request=request,
        name="pdf_tools_page.html",
        context={"output_files": outputs}
    )
    