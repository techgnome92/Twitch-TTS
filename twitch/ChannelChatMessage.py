from typing import List
from twitchAPI.object.eventsub import Subscription, ChannelChatMessageData, ChatMessageBadge
from twitchAPI.object.base import TwitchObject


class ChannelChatMessageSourceBroadcasterData(ChannelChatMessageData):
    # add messages source broadcaster data for shared chat
    source_broadcaster_user_id: str
    source_broadcaster_user_name: str
    source_broadcaster_user_login: str
    source_message_id: str
    source_badges: List[ChatMessageBadge]


class ChannelChatMessageSourceEvent(TwitchObject):
    # add messages source broadcaster data for shared chat to event
    subscription: Subscription
    event: ChannelChatMessageSourceBroadcasterData
