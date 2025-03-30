import pyttsx3

ms_voice_prefix = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens"


def tts(filepath, message, rate=120, volume=100, voice="MSSam"):
    engine = pyttsx3.init()
    engine.setProperty("voice", f"{ms_voice_prefix}\\{voice}")
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    engine.save_to_file(message, filepath)

    engine.runAndWait()
