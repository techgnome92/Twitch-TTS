from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from validate import Settings
from utils import settings, save_json, voices, allowed_users, ignored_users, ignored_words, replace_words, regex_filter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from __twitch.twitch import run_twitch

templates = Jinja2Templates(directory="templates")


TTS_RUNNING: bool = False

lifespan_events = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    lifespan_events["eventsub"], lifespan_events["twitch"] = await run_twitch()
    print("Bot is starting up")
    yield
    await lifespan_events["eventsub"].stop()
    await lifespan_events["twitch"].close()
    print("Bot is shutting down")

app = FastAPI(lifespan=lifespan)


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
            "ignored_words": ignored_words,
            "replace_words": replace_words,
            "regex_filters": regex_filter,
            "TTS_RUNNING": TTS_RUNNING
        },
    )


@app.post("/toggle_play")
def toggle_play(on: dict):
    global TTS_RUNNING
    TTS_RUNNING = bool(on)


@app.post("/update_validation")
def update_validation(v: Settings):
    global settings

    settings = v
    settings.TTS_VOICE = settings.TTS_VOICE.lower()
    save_json(settings.model_dump(mode="json"), "settings.json")


# ALLOWED USERS
@app.post("/allowed_users")
def update_allowed_users(users: dict[str, str]):
    global allowed_users
    allowed_users = users
    save_json(allowed_users, "users/allowed.json")


@app.get("/allowed_user_row")
def add_allowed_user_row(request: Request):
    return templates.TemplateResponse(request, "users/allowed_user_row.html", context={"voices": voices})


# IGNORE USERS
@app.post("/ignored_users")
def update_ignored_users(users: dict[str, list]):
    global ignored_users
    ignored_users = set(users["users"]) if "users" not in users else []
    save_json(list(ignored_users), "users/ignored.json")


@app.get("/ignored_user_row")
def add_ignored_user_row(request: Request):
    return templates.TemplateResponse(request, "users/ignored_user_row.html")


# FILTER MESSAGE
@app.post("/ignored_words")
def update_word_ignore(words: dict[str, list]):
    global ignored_words
    ignored_words = set(words["words"]) if "words" in words else []
    save_json(list(ignored_words), "filters_json/word_ignore.json")


@app.get("/ignored_words_row")
def add_ignored_word_row(request: Request):
    return templates.TemplateResponse(request, "filters_json/ignored_word_row.html")


@app.post("/replace_words")
def update_replace_words(words: dict[str, str]):
    global replace_words
    replace_words = words
    save_json(replace_words, "filters_json/word_replace.json")


@app.get("/word_replace_row")
def add_word_replace_row(request: Request):
    return templates.TemplateResponse(request, "filters_json/word_replace_row.html")


@app.post("/regex_filter")
def update_regex_filter(regex: dict[str, list]):
    global regex_filter
    regex_filter = set(regex["regex"])
    save_json(list(regex_filter), "filters_json/regex_filters.json")


@app.get("/regex_filter_row")
def add_regex_filter_row(request: Request):
    return templates.TemplateResponse(request, "filters_json/regex_filter_row.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
