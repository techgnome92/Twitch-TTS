import json
from validate import Validation


def load_json(fp: str):
    with open(fp, "r") as f:
        return json.load(f)


def save_json(data, fp: str) -> None:
    with open(fp, "w") as f:
        json.dump(data, f, indent=4)


settings = load_json("config.json")
validation = Validation(**load_json("validation.json"))
