from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import template_env
from tools import TOOLS
import mimetypes

mimetypes.add_type("application/javascript", ".mjs")
mimetypes.add_type("application/wasm", ".wasm")


app = FastAPI()
app.mount("/static", StaticFiles(directory=template_env.BASE_DIR / "static"), name="static")
app.mount("/output", StaticFiles(directory=template_env.OUTPUT_DIR), name="output")

template_env.templates = template_env.build_templates(TOOLS)

for tool in TOOLS:
    app.include_router(tool.router, prefix=f"/tools/{tool.meta['slug']}")

@app.get("/")
def index(request: Request):
    return template_env.templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tools": [t.meta for t in TOOLS]},
    )