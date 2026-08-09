from fastapi import APIRouter, Request
import template_env
    
router = APIRouter()

@router.get("/")
def page(request: Request):
    return template_env.templates.TemplateResponse(
        request=request,
        name="collage_page.html",
        context={},
    )