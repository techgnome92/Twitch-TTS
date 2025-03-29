import pyttsx3
import os
from utils import voices as voice_options
import re

ms_voice_prefix = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens"

path = f"{os.getcwd()}\\dectalk"
os.add_dll_directory(f"{path}")


def generate_wav(filepath, message, rate=120, volume=100, voice="microsoft|sam"):
    v = voice.split("|")
    better_name_needed[v[0]](filepath, message, rate, volume, voice_options[voice])


def microsoft_tts(filepath, message, rate=120, volume=100, voice="MSSam"):
    engine = pyttsx3.init()
    engine.setProperty("voice", f"{ms_voice_prefix}\\{voice}")
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    engine.save_to_file(message, filepath)

    engine.runAndWait()


def dectalk_tts(filepath, message, rate=120, volume=100, voice="Paul"):
    message = message.replace('"', "").replace("&", "").replace("|", "").replace(";", "")
    message = re.sub(r"\[:.+?\]", "", message)
    os.system(
        f'dectalk\\say.exe -d dtalk_us.dic -w {filepath} "[:phoneme on] [:name {voice}] [:rate {rate}] {message}"'
    )


better_name_needed = {"microsoft": microsoft_tts, "dectalk": dectalk_tts}


if __name__ == "__main__":

    message = "This is a message"

    generate_wav("ms.wav", message=message, voice="microsoft|zira")
    generate_wav("dectalk.wav", message=message, voice="dectalk|kit")
