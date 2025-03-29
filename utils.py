import json
from pydantic import BaseModel


class Settings(BaseModel):
    BROADCASTER_ALLOWED: bool = False
    SUBSCRIBERS_ALLOWED: bool = False
    VIP_ALLOWED: bool = False
    TURBO_ALLOWED: bool = False
    MODERATOR_ALLOWED: bool = False
    BIT_DONATION_ALLOWED: bool = False
    BIT_DONATION_AMOUNT: int = 100
    CHANNEL_POINT_ALLOWED: bool = False
    CHANNEL_POINT_ID: str = ""
    EVERYONE_ALLOWED: bool = False
    SAY_CHEER_EMOTE: bool = False
    SAY_USERNAME: bool = False
    READ_SHARED_CHAT: bool = False
    TTS_VOICE: str = "microsoft|sam"
    TTS_RATE: int = 120


def load_json(fp: str):
    with open(fp, "r") as f:
        return json.load(f)


def save_json(data, fp: str) -> None:
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)


secrets = load_json("settings/config.json")
settings = Settings(**load_json("settings/settings.json"))
voices = load_json("voices.json")

ignored_users = load_json("users/ignored.json")
allowed_users = load_json("users/allowed.json")

ignored_words = load_json("filters_json/word_ignore.json")
replace_words = load_json("filters_json/word_replace.json")
regex_filter = load_json("filters_json/regex_filters.json")
