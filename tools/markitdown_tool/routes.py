from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from tools.markitdown_tool.helpers import validateInputFileType
from .logic import convertToMarkdown
import template_env   # ← the module, not the name

from .helpers import validateInputFileType, validateInputFileSize

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

    if not validateInputFileType(file.filename, file.content_type):
            return template_env.templates.TemplateResponse(
            request=request,
            name="page.html",
            context={"error": "Invalid file type. Only PDF and DOCX files are allowed."}
        )

    if not validateInputFileSize(file.file):
        return template_env.templates.TemplateResponse(
            request=request,
            name="page.html",
            context={"error": "File size exceeds the limit."}
        )

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