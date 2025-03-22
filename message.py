from twitchAPI.object.eventsub import ChannelChatMessageEvent
from validate import validate_message, Settings
from filters import filter_message
from utils import settings, allowed_users, ignored_users, ignored_words, replace_words, regex_filter


class Message:
    settings: Settings = settings

    allowed_users: list = allowed_users
    ignored_users: list = ignored_users
    regex_filter: list = regex_filter
    ignored_words: list = ignored_words
    replace_words: dict = replace_words

    def __init__(self, data: ChannelChatMessageEvent):
        self.data = data
        self.message = data.event.message
        self.is_valid = self.validate()
        self.text = self.filter_message()

    def validate(self):
        return validate_message(self.data, self.settings, self.allowed_users, self.ignored_users)

    def filter_message(self) -> str:
        if self.is_valid:
            return filter_message(self.message, self.ignored_words, self.replace_words, self.regex_filter)
        return ""
