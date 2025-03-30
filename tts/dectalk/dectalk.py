import os
import re

relative_path = "tts\\dectalk"

path = f"{os.getcwd()}\\{relative_path}"
os.add_dll_directory(f"{path}")


def tts(filepath, message, rate=120, volume=100, voice="Paul"):
    print("TESTING")
    message = message.replace('"', "").replace("&", "").replace("|", "").replace(";", "")
    message = re.sub(r"\[:.+?\]", "", message)
    os.system(
        f'{relative_path}\\say.exe -d dtalk_us.dic -w {filepath} "[:phoneme on] [:name {voice}] [:rate {rate}] {message}"'
    )
