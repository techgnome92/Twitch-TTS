from fastapi import FastAPI, Request
from validate import Settings
from utils import settings, save_json, voices, allowed_users
from allowed_user import AllowedUsersList
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


@app.post("/allowed_users")
def update_allowed_users(users: AllowedUsersList):
    new_dict: dict = {}
    for i in users.users:
        new_dict[i.username] = i.voice

    save_json(new_dict, "users/allowed.json")


@app.get("/allowed_user_row/{_id}")
def add_allowed_user_row(request: Request, _id: int):
    return templates.TemplateResponse(request, "allowed_user.html", context={"voices": voices, "id": _id})


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request, "index.html", context={"settings": settings, "voices": voices, "allowed_users": allowed_users}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
