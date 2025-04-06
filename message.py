from twitch.ChannelChatMessage import ChannelChatMessageSourceEvent
from validate import validate_message, Settings
from filters import filter_message
from utils import (
    settings,
    secrets,
    allowed_users,
    ignored_users,
    ignored_words,
    replace_words,
    regex_filter,
    voices as voice_options,
    save_json,
)
import os, uuid  # noqa
from tts.tts import generate_wav
import simpleaudio as sa
import keyboard

if secrets["SILENCE_HOTKEY"]:
    keyboard.add_hotkey(secrets["SILENCE_HOTKEY"], sa.stop_all)


class Message:
    settings: Settings = settings

    allowed_users: list = allowed_users
    ignored_users: list = ignored_users
    regex_filter: list = regex_filter
    ignored_words: list = ignored_words
    replace_words: dict = replace_words
    TTS_RUNNING: bool = False
    player = None

    def __init__(self, data: ChannelChatMessageSourceEvent):
        self.data = data
        self.user = data.event.chatter_user_name
        self.message = data.event.message
        self.is_valid = self.validate()
        self.text = self.filter_message()
        self.rate = self.settings.TTS_RATE
        self.volume = 100
        self.voice = self.get_voice()
        self.file = f"{str(uuid.uuid1())}.wav"
        self.play_object = None

    def validate(self):
        if self.TTS_RUNNING:
            return validate_message(self.data, self.settings, self.allowed_users, self.ignored_users)
        else:
            return False

    def filter_message(self) -> str:
        if self.is_valid:
            return filter_message(
                self.message, self.user, self.ignored_words, self.replace_words, self.regex_filter, Message.settings
            )
        return ""

    def get_voice(self):
        _voice = self.settings.TTS_VOICE

        if self.user in self.allowed_users:
            if self.allowed_users[self.user][0] in voice_options:
                _voice = self.allowed_users[self.user][0]
        self.voice = _voice

    def say_message(self):

        self.get_voice()
        generate_wav(self.file, self.text, rate=self.rate, voice=self.voice)

        wave_obj = sa.WaveObject.from_wave_file(self.file)
        self.play_object = wave_obj.play()
        Message.player = self.play_object
        os.remove(self.file)

    # def save_text_to_file(self):
    #     save_json(self.data.to_dict(include_none_values=True), secrets["LATEST_MESSAGE_JSON"])

    def choose_mode(self):
        if Message.settings.MODE == "keepup":
            if not Message.player or not Message.player.is_playing():
                # self.save_text_to_file()
                self.say_message()

        elif Message.settings.MODE == "multi":
            self.say_message()

        else:
            # self.save_text_to_file()
            self.say_message()
            self.play_object.wait_done()
