from fastapi import APIRouter, Request, UploadFile, File
import template_env
from .logic import getPdfMetadata

router = APIRouter()

@router.get("/")
def page(request: Request):
    return template_env.templates.TemplateResponse(
        request=request,
        name="pdf_tools_page.html",
        context={},
    )

@router.post("/")
def handle_upload(request: Request, files: list[UploadFile] = File(...)):
    # Handle the uploaded files here
    metadata_list = []
    for file in files:
        # Process each uploaded file
        metadata = getPdfMetadata(file.file)
        # Do something with the metadata, e.g., save it to a database or return it
        metadata_list.append(metadata)
    return template_env.templates.TemplateResponse(
        request=request,
        name="pdf_tools_page.html",
        context={"metadata_list": metadata_list},
    )
