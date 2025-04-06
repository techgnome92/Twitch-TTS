# Description
Twitch text-to-speech bot is a bot that reads out chat messages using DECTalk or Microsoft Voices.

# Installation
Install the requirements with `python -m pip install -r requirements.txt`

To install Windows XP voices (Sam, Mike, Mary) run `WinXP_TTS_Voices_v1.3.exe` in `tts/microsoft`
* Install at your own risk

# Setup
## Register Twitch Application
Follow the instructions at https://dev.twitch.tv/docs/authentication/register-app/ 


OAuth Redirect URLs
- http://localhost:17563
- http://localhost:3000

Category - Chat Bot

## Configure
Update `config example.json` and rename to `config.json` in settings folder

- APPLICATION_NAME - Name of Application from twitch dev console
- CLIENT_ID - Client ID from twitch dev console
- CLIENT_SECRET - Client Secret from twitch dev console


- BROADCASTER_USER_ID - ID of the account whose chat you want to read
- CHATTER_USER_ID - ID of the account you want to read chat. This can be the same as BROADCASTER_USER_ID

Get your Channel ID from https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/



# Run
Use `python main.py` for access to the full GUI interface at localhost:8000

Use `python twitch/twitch.py` to run a GUIless version. Note: This does not allow updating any settings, user lists, or filters  while running