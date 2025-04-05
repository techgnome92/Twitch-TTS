import re
from twitchAPI.object.eventsub import ChatMessage
from validate import Settings


def filter_message(
    message: ChatMessage,
    username: str,
    ignored_words: list,
    replaced_words: dict,
    regex_filter: list,
    settings: Settings,
):

    message = construct_message(message=message, username=username, settings=settings)

    message = filter_words(message, ignored_words)
    message = filter_words(message, regex_filter)
    message = replace_words(message, replaced_words)

    return message


def filter_words(message: str, filters: list) -> str:
    for pattern in filters:
        message = re.sub(pattern, "", message, flags=re.IGNORECASE)

    return message


def replace_words(message: str, filters: dict) -> str:
    for phrase, replacement in filters.items():
        message = re.sub(phrase, replacement, message, flags=re.IGNORECASE)

    return message


def add_username(message: str, username: str):
    return f"{username} says {message}"


def construct_message(message: ChatMessage, username: str, settings: Settings):
    # Build message from the message fragments
    text = ""
    for frag in message.fragments:
        if frag.type == "cheermote":
            if not settings.SAY_CHEER_EMOTE:
                continue

        text += frag.text

    if settings.SAY_USERNAME:
        text = add_username(text, username)

    return text
