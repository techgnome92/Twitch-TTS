from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from validate import Settings
from utils import save_json, voices
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from twitch.twitch import run_twitch
from message import Message
import simpleaudio as sa
import os
import signal
import webbrowser
from utils import secrets

templates = Jinja2Templates(directory="templates")


Message.TTS_RUNNING = False

lifespan_events = {}


async def shutdown(lifespan_events: dict):
    await lifespan_events["eventsub"].stop()
    await lifespan_events["twitch"].close()
    print("Bot is shutting down")


@asynccontextmanager
async def lifespan(app: FastAPI):
    lifespan_events["eventsub"], lifespan_events["twitch"] = await run_twitch()
    webbrowser.open(f"http://localhost:{secrets['PORT']}/", new=2)
    print("Bot is starting up")
    yield
    await shutdown(lifespan_events)


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "settings": Message.settings,
            "voices": voices,
            "allowed_users": Message.allowed_users,
            "ignored_users": Message.ignored_users,
            "ignored_words": Message.ignored_words,
            "replace_words": Message.replace_words,
            "regex_filters": Message.regex_filter,
            "TTS_RUNNING": Message.TTS_RUNNING,
        },
    )


@app.post("/toggle_play")
def toggle_play(on: dict):
    Message.TTS_RUNNING = bool(on)
    if Message.TTS_RUNNING is False:
        sa.stop_all()


@app.post("/skip_message")
def skip_message():
    sa.stop_all()


@app.post("/quit")
def quit_program():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)


@app.post("/update_validation")
def update_validation(_settings: Settings):
    Message.settings = _settings
    Message.settings.TTS_VOICE = _settings.TTS_VOICE.lower()
    save_json(Message.settings.model_dump(mode="json"), "settings/settings.json")


# ALLOWED USERS
@app.post("/allowed_users")
def update_allowed_users(users: dict[str, tuple[str, bool]]):
    Message.allowed_users = users
    save_json(Message.allowed_users, "data/users/allowed.json")


@app.get("/allowed_user_row")
def add_allowed_user_row(request: Request):
    return templates.TemplateResponse(request, "users/allowed_user_row.html", context={"voices": voices})


# IGNORE USERS
@app.post("/ignored_users")
def update_ignored_users(users: dict[str, list]):
    Message.ignored_users = set(users["users"]) if "users" in users else []
    save_json(list(Message.ignored_users), "data/users/ignored.json")


@app.get("/ignored_user_row")
def add_ignored_user_row(request: Request):
    return templates.TemplateResponse(request, "users/ignored_user_row.html")


# FILTER MESSAGE
@app.post("/ignored_words")
def update_word_ignore(words: dict[str, list]):
    Message.ignored_words = set(words["words"]) if "words" in words else []
    save_json(list(Message.ignored_words), "data/filters/word_ignore.json")


@app.get("/ignored_words_row")
def add_ignored_word_row(request: Request):
    return templates.TemplateResponse(request, "filters/ignored_word_row.html")


@app.post("/replace_words")
def update_replace_words(words: dict[str, str]):
    Message.replace_words = words
    save_json(Message.replace_words, "data/filters/word_replace.json")


@app.get("/word_replace_row")
def add_word_replace_row(request: Request):
    return templates.TemplateResponse(request, "filters/word_replace_row.html")


@app.post("/regex_filter")
def update_regex_filter(regex: dict[str, list]):
    Message.regex_filter = set(regex["regex"]) if "regex" in regex else []
    save_json(list(Message.regex_filter), "data/filters/regex_filters.json")


@app.get("/regex_filter_row")
def add_regex_filter_row(request: Request):
    return templates.TemplateResponse(request, "filters/regex_filter_row.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=secrets["PORT"])
