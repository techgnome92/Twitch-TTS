import json
from validate import Settings
from allowed_user import AllowedUsersList


def load_json(fp: str):
    with open(fp, "r") as f:
        return json.load(f)


def save_json(data, fp: str) -> None:
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)


secrets = load_json("config.json")
settings = Settings(**load_json("settings.json"))
allowed_users = AllowedUsersList(**load_json("users/allowed.json")).users
voices = load_json("voices.json")
