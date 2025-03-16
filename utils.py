import json
from validate import Settings
from allowed_user import AllowedUser


def load_json(fp: str):
    with open(fp, "r") as f:
        return json.load(f)


def save_json(data, fp: str) -> None:
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)


secrets = load_json("config.json")
settings = Settings(**load_json("settings.json"))
voices = load_json("voices.json")

_allowed_users = load_json("users/allowed.json")
allowed_users = [AllowedUser(username=k, voice=v) for k, v in _allowed_users.items()]
