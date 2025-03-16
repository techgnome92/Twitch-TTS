from fastapi import FastAPI, Request
from validate import Settings
from utils import settings, save_json, voices
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.post("/update_validation")
def update_validation(v: Settings):
    global settings

    settings = v
    settings.TTS_VOICE = settings.TTS_VOICE.lower()
    save_json(settings.model_dump(mode="json"), "settings.json")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "index.html", context={"settings": settings, "voices": voices})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
