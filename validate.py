from twitchAPI.object.eventsub import ChannelChatMessageEvent
from pydantic import BaseModel


class Settings(BaseModel):
    BROADCASTER_ALLOWED: bool = False
    SUBSCRIBERS_ALLOWED: bool = False
    VIP_ALLOWED: bool = False
    TURBO_ALLOWED: bool = False
    MODERATOR_ALLOWED: bool = False
    BIT_DONATION_ALLOWED: bool = False
    BIT_DONATION_AMOUNT: int = 100
    CHANNEL_POINT_ALLOWED: bool = False
    CHANNEL_POINT_ID: str = ""
    EVERYONE_ALLOWED: bool = False
    SAY_CHEER_EMOTE: bool = False
    SAY_USERNAME: bool = False
    TTS_VOICE: str = "ms_sam"


def validate_message(message: ChannelChatMessageEvent, settings: Settings, users_allowed: list, users_ignored: list):
    event = message.event
    badges = [badge.set_id for badge in event.badges]

    if not message:
        return False

    if event.chatter_user_login == users_ignored:
        return False

    if event.chatter_user_login == users_allowed:
        return True

    if settings.EVERYONE_ALLOWED:
        return True

    if settings.BROADCASTER_ALLOWED:
        if "broadcaster" in badges:
            return True

    if settings.VIP_ALLOWED:
        if "vip" in badges:
            return True

    if settings.TURBO_ALLOWED:
        if "turbo" in badges:
            return True

    if settings.MODERATOR_ALLOWED:
        if "moderator" in badges:
            return True

    if settings.BIT_DONATION_ALLOWED:
        if event.cheer:
            return event.cheer.bits >= settings.BIT_DONATION_AMOUNT

    if settings.CHANNEL_POINT_ALLOWED:
        if event.channel_points_custom_reward_id == settings.CHANNEL_POINT_ID:
            return True

    return False
