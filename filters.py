import re
from twitchAPI.object.eventsub import ChatMessage


def filter_message(message: ChatMessage, ignored_words: list, replaced_words: dict, regex_filter: list):
    message = message.text

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
