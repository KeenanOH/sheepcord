import datetime
import enum
import typing

import pydantic

from sheepcord import snowflake, permissions
from sheepcord.models import users

__all__: typing.Sequence[str] = (
    "ChannelType",
    "ChannelMention",
    "VideoQualityMode",
    "ThreadMetadata",
    "ThreadMember",
    "ChannelFlag",
    "Channel",
)


class ChannelType(enum.IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15


class ChannelMention(pydantic.BaseModel):
    id: snowflake.Snowflake
    guild_id: snowflake.Snowflake
    type: ChannelType
    name: str


class VideoQualityMode(enum.IntEnum):
    AUTO = 1
    FULL = 2


class ThreadMetadata(pydantic.BaseModel):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: datetime.datetime
    locked: bool
    invitable: typing.Optional[bool]
    create_timestamp: typing.Optional[datetime.datetime]


class ThreadMember(pydantic.BaseModel):
    id: typing.Optional[snowflake.Snowflake]
    user_id: typing.Optional[snowflake.Snowflake]
    join_timestamp: snowflake.Snowflake
    flags: int  # Any user-thread settings? is there an enum for this?


class ChannelFlag(enum.IntFlag):
    PINNED = 1 << 1


class Channel(pydantic.BaseModel):
    id: snowflake.Snowflake
    type: ChannelType
    guild_id: typing.Optional[snowflake.Snowflake]
    position: typing.Optional[int]
    permission_overwrites: typing.Optional[list[permissions.Overwrite]]
    name: typing.Optional[str]
    topic: typing.Optional[str]
    nsfw: typing.Optional[bool]
    last_message_id: typing.Optional[snowflake.Snowflake]
    bitrate: typing.Optional[int]
    user_limit: typing.Optional[int]
    rate_limit_per_user: typing.Optional[int]
    recipients: typing.Optional[list[users.User]]
    icon: typing.Optional[str]
    owner_id: typing.Optional[snowflake.Snowflake]
    application_id: typing.Optional[snowflake.Snowflake]
    parent_id: typing.Optional[snowflake.Snowflake]
    last_pin_timestamp: typing.Optional[datetime.datetime]
    rtc_region: typing.Optional[str]
    video_quality_mode: typing.Optional[VideoQualityMode]
    message_count: typing.Optional[int]
    member_count: typing.Optional[int]
    thread_metadata: typing.Optional[ThreadMetadata]
    member: typing.Optional[ThreadMember]
    default_auto_archive_duration: typing.Optional[int]
    permissions: typing.Optional[permissions.Permissions]
    flags: typing.Optional[ChannelFlag]
