import datetime
import enum
import typing

import pydantic

from sheepcord import snowflake
from sheepcord.models import (
    users,
    roles,
    attachments,
    embeds,
    channels,
    reactions,
    applications,
    members,
    stickers,
    components,
)

__all__: typing.Sequence[str] = (
    "MessageType",
    "MessageActivityType",
    "MessageActivity",
    "MessageReference",
    "MessageFlag",
    "MessageInteraction",
    "Message",
)


class MessageType(enum.IntEnum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24


class MessageActivityType(enum.IntEnum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageActivity(pydantic.BaseModel):
    type: MessageActivityType
    party_id: typing.Optional[str]


class MessageReference(pydantic.BaseModel):
    message_id: typing.Optional[snowflake.Snowflake]
    channel_id: typing.Optional[snowflake.Snowflake]
    guild_id: typing.Optional[snowflake.Snowflake]
    fail_if_not_exists: typing.Optional[snowflake.Snowflake]


class MessageFlag(enum.IntFlag):
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8


class MessageInteraction(pydantic.BaseModel):
    id: snowflake.Snowflake
    type: int
    name: str
    user: users.User
    member: typing.Optional[members.Member]


class Message(pydantic.BaseModel):
    id: snowflake.Snowflake
    channel_id: snowflake.Snowflake
    author: users.User
    content: str
    timestamp: datetime.datetime
    edited_timestamp: typing.Optional[datetime.datetime]
    tts: bool
    mention_everyone: bool
    mentions: list[users.User]
    mention_roles: list[roles.Role]
    mention_channels: typing.Optional[channels.ChannelMention]
    attachments: list[attachments.Attachment]
    embeds: list[embeds.Embed]
    reactions: typing.Optional[list[reactions.Reaction]]
    noice: typing.Optional[typing.Union[int, str]]
    pinned: bool
    webhook_id: typing.Optional[snowflake.Snowflake]
    type: MessageType
    activity: typing.Optional[MessageActivity]
    application: typing.Optional[applications.Application]
    application_id: typing.Optional[snowflake.Snowflake]
    message_reference: typing.Optional[MessageReference]
    flags: MessageFlag
    interaction: typing.Optional[MessageInteraction]
    thread: typing.Optional[channels.Channel]
    components: typing.Optional[
        typing.Union[
            components.ActionRow,
            components.Button,
            components.SelectMenu,
            components.TextInput,
        ]
    ]
    sticker_items: typing.Optional[list[stickers.StickerItem]]
    stickers: typing.Optional[list[stickers.Sticker]]
