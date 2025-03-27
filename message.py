from twitch.ChannelChatMessage import ChannelChatMessageSourceEvent
from validate import validate_message, Settings
from filters import filter_message
from utils import (
    settings,
    allowed_users,
    ignored_users,
    ignored_words,
    replace_words,
    regex_filter,
    voices as voice_options,
)
import os, uuid  # noqa
from tts import generate_wav
import simpleaudio as sa


class Message:
    settings: Settings = settings

    allowed_users: list = allowed_users
    ignored_users: list = ignored_users
    regex_filter: list = regex_filter
    ignored_words: list = ignored_words
    replace_words: dict = replace_words
    TTS_RUNNING: bool = False

    def __init__(self, data: ChannelChatMessageSourceEvent):
        self.data = data
        self.user = data.event.chatter_user_name
        self.message = data.event.message
        self.is_valid = self.validate()
        self.text = self.filter_message()
        self.rate = self.settings.TTS_RATE
        self.volume = 100

    def validate(self):
        if self.TTS_RUNNING:
            return validate_message(self.data, self.settings, self.allowed_users, self.ignored_users)
        else:
            return False

    def filter_message(self) -> str:
        if self.is_valid:
            return filter_message(self.message, self.ignored_words, self.replace_words, self.regex_filter)
        return ""

    def say_message(self):
        session = str(uuid.uuid1())
        temp_file = f"{session}.wav"

        voice = self.settings.TTS_VOICE
        if self.user in self.allowed_users:
            if self.allowed_users[self.user][0] in voice_options:
                voice = self.allowed_users[self.user]

        generate_wav(temp_file, self.text, rate=self.rate, voice=voice)

        wave_obj = sa.WaveObject.from_wave_file(temp_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        os.remove(temp_file)
