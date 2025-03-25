from typing import List
from twitchAPI.object.eventsub import ChannelChatMessageData, ChatMessageBadge
from twitchAPI.object.base import TwitchObject


class ChannelChatMessageSourceBroadcasterData(ChannelChatMessageData):
    source_broadcaster_user_id: str
    source_broadcaster_user_name: str
    source_broadcaster_user_login: str
    source_message_id: str
    source_badges: List[ChatMessageBadge]


class ChannelChatMessageSourceBroadcasterEvent(TwitchObject):
    event: ChannelChatMessageSourceBroadcasterData
