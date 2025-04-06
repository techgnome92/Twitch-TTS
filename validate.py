from twitch.ChannelChatMessage import ChannelChatMessageSourceEvent
from utils import Settings


def validate_message(
    message: ChannelChatMessageSourceEvent, settings: Settings, users_allowed: list, users_ignored: list
):
    event = message.event
    badges = [badge.set_id for badge in event.badges]

    if not message:
        return False

    if settings.READ_SHARED_CHAT is False:
        if event.source_broadcaster_user_name:
            return False

    if event.chatter_user_name in users_ignored:
        return False

    if event.chatter_user_name in users_allowed:
        if users_allowed[event.chatter_user_name][1] is True:
            return True

    if settings.EVERYONE_ALLOWED:
        return True

    if settings.BROADCASTER_ALLOWED:
        if "broadcaster" in badges:
            return True

    if settings.SUBSCRIBERS_ALLOWED:
        if "subscriber" in badges:
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
