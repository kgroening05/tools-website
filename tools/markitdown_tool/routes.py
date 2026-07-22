from fastapi import APIRouter, Request, UploadFile, File
from .logic import convertToMarkdown
import template_env   # ← the module, not the name

router = APIRouter()

@router.get("/")
def page(request: Request):
    return template_env.templates.TemplateResponse(
        request=request,
        name="page.html",
        context={},
    )

@router.post("/convert")
def convert(request: Request, file: UploadFile = File(...)):
    markdown = convertToMarkdown(
        file.file,
        file.filename or "unknown",
        file.content_type or None,
    )
    return template_env.templates.TemplateResponse(
        request=request,
        name="page.html",
        context={"markdown": markdown, "filename": file.filename},
    )