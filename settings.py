import json


def load_json(fp: str):
    with open(fp, "r") as f:
        return json.load(f)


def save_json(fp: str):
    with open(fp, "r") as f:
        return json.dump(f, indent=4)


settings = load_json("config.json")
