from twitchAPI.object.eventsub import ChannelChatMessageEvent
from validate import validate_message, Validation


class Message:
    settings: Validation = Validation()

    user_allow_list: list = []
    user_ignore_list: list = []
    regex_filter: list = []
    word_filter: list = []
    word_replacement: dict = {}

    def __init__(self, message: ChannelChatMessageEvent):
        self.message = message

    def validate(self):
        validate_message(self.message, self.settings, self.user_allow_list, self.user_ignore_list)
