from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope
from twitchAPI.eventsub.websocket import EventSubWebsocket
from __twitch.ChannelChatMessage import ChannelChatMessageSourceEvent

import asyncio
from utils import secrets

SCOPES = [AuthScope.USER_READ_CHAT]


async def on_message(message):
    # event = message.event
    print(message.__dict__)


async def run_twitch():
    twitch = await Twitch(secrets["CLIENT_ID"], secrets["CLIENT_SECRET"])
    helper = UserAuthenticationStorageHelper(twitch, SCOPES)
    await helper.bind()

    eventsub = EventSubWebsocket(twitch)
    eventsub.start()

    param = {
        'broadcaster_user_id': secrets["BROADCASTER_USER_ID"],
        'user_id': secrets["CHATTER_USER_ID"]
    }
    await eventsub._subscribe('channel.chat.message', '1', param, on_message, ChannelChatMessageSourceEvent)
    return eventsub, twitch
    # try:
    #     wait_for_user_input()
    # finally:
    #     print("The bot is shutting down")
    #     await eventsub.stop()
    #     await twitch.close()


async def exit_application(eventsub, twitch):
    await eventsub.stop()
    await twitch.close()


def wait_for_user_input():
    print("The bot is running")
    input("press ENTER to close\n")


if __name__ == "__main__":
    asyncio.run(run_twitch())
