from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, Environment, FileSystemLoader

from tools import TOOLS

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

loader = ChoiceLoader(
    [FileSystemLoader(BASE_DIR / "templates")]
    + [
        FileSystemLoader(BASE_DIR / "tools" / tool.__name__.rsplit(".", 1)[-1] / "templates")
        for tool in TOOLS
    ]
)
env = Environment(loader=loader)
env.globals["all_tools"] = [tool.meta for tool in TOOLS]
templates = Jinja2Templates(env=env)

for tool in TOOLS:
    app.include_router(tool.router, prefix=f"/tools/{tool.meta['slug']}")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request, "index.html", {"tools": [tool.meta for tool in TOOLS]}
    )
