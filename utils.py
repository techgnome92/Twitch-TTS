import json
from validate import Settings


def load_json(fp: str):
    with open(fp, "r") as f:
        return json.load(f)


def save_json(data, fp: str) -> None:
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)


secrets = load_json("config.json")
settings = Settings(**load_json("settings.json"))
voices = load_json("voices.json")

ignored_users = load_json("users/ignored.json")
allowed_users = load_json("users/allowed.json")

ignored_words = load_json("filters_json/word_ignore.json")
replace_words = load_json("filters_json/word_replace.json")
regex_filter = load_json("filters_json/regex_filters.json")
