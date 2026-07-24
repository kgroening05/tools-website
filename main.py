from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import template_env
from tools import TOOLS

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

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