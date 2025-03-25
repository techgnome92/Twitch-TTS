import pyttsx3

ms_voice_prefix = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens"


def generate_wav(filepath, message, rate=120, volume=100, voice="MSSam"):

    engine = pyttsx3.init()
    engine.setProperty("voice", f"{ms_voice_prefix}\\{voice}")
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    engine.save_to_file(message, filepath)

    engine.runAndWait()


if __name__ == "__main__":

    message = "This is a message for words per minute testing because it's interesting to me"
    for i in range(0, 20+1):
        generate_wav(f"temp {i*10}.wav", message=message, rate=i*10)
