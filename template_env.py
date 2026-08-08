from pathlib import Path
import shutil
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def build_templates(tools):
    loader = ChoiceLoader(
        [FileSystemLoader(BASE_DIR / "templates")]
        + [
            FileSystemLoader(BASE_DIR / "tools" / t.__name__.rsplit(".", 1)[-1] / "templates")
            for t in tools
        ]
    )
    env = Environment(loader=loader)
    env.globals["all_tools"] = [t.meta for t in tools]
    return Jinja2Templates(env=env)

templates = None  # module-level, assigned by main.py at startup

def get_templates():
    return templates