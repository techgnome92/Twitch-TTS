from fastapi import FastAPI, Request
from validate import Settings
from utils import settings, save_json, voices, allowed_users, _allowed_users, ignored_users
from allowed_user import AllowedUsersList, AllowedUser, IgnoreUsersList
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "settings": settings,
            "voices": voices,
            "allowed_users": allowed_users,
            "ignored_users": ignored_users,
        },
    )


@app.post("/update_validation")
def update_validation(v: Settings):
    global settings

    settings = v
    settings.TTS_VOICE = settings.TTS_VOICE.lower()
    save_json(settings.model_dump(mode="json"), "settings.json")


# ALLOWED USERS
@app.post("/allowed_users")
def update_allowed_users(users: AllowedUsersList):
    new_dict: dict = {}
    for i in users.users:
        if i is None:
            continue
        new_dict[i.username] = i.voice
    save_json(new_dict, "users/allowed.json")


@app.get("/allowed_user_row")
def add_allowed_user_row(request: Request, _id: int):
    return templates.TemplateResponse(request, "allowed_user_row.html", context={"voices": voices, "id": _id})


@app.delete("/allowed_users/{username:str}")
def delete_allowed_user(request: Request, username: str):
    global allowed_users, _allowed_users
    del _allowed_users[username]
    allowed_users = [AllowedUser(username=k, voice=v) for k, v in _allowed_users.items()]
    save_json(_allowed_users, "users/allowed.json")
    return templates.TemplateResponse(request, "delete.html")


# IGNORE USERS
@app.post("/ignored_users")
def update_ignored_users(users: IgnoreUsersList):
    save_json(users.users, "users/ignored.json")


@app.get("/ignored_user_row")
def add_ignored_user_row(request: Request):
    return templates.TemplateResponse(request, "ignored_user_row.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
