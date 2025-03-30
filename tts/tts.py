from utils import voices as voice_options
from .microsoft import ms
from .dectalk import dectalk


def generate_wav(filepath, message, rate=120, volume=100, voice="microsoft|sam"):
    v = voice.split("|")
    print(v[0])
    tts_systems[v[0]](filepath, message, rate, volume, voice_options[voice])


tts_systems = {"microsoft": ms.tts, "dectalk": dectalk.tts}


if __name__ == "__main__":

    message = "This is a message"

    generate_wav("ms.wav", message=message, voice="microsoft|zira")
    generate_wav("dectalk.wav", message=message, voice="dectalk|kit")
