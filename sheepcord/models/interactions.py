from __future__ import annotations

import enum
import typing

import pydantic

from sheepcord import snowflake
from sheepcord.models import commands
from sheepcord.models import (
    responses,
    members,
    users,
    messages,
    roles,
    channels,
    attachments,
)

__all__: typing.Sequence[str] = (
    "InteractionType",
    "ResolvedData",
    "InteractionOption",
    "InteractionData",
    "Interaction",
    "InteractionCallbackType",
    "InteractionResponse",
)


class InteractionType(enum.IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class ResolvedData(pydantic.BaseModel):
    users: typing.Optional[dict[snowflake.Snowflake, users.User]]
    members: typing.Optional[dict[snowflake.Snowflake, members.Member]]
    roles: typing.Optional[dict[snowflake.Snowflake, roles.Role]]
    channels: typing.Optional[dict[snowflake.Snowflake, channels.Channel]]
    messages: typing.Optional[dict[snowflake.Snowflake, messages.Message]]
    attachments: typing.Optional[dict[snowflake.Snowflake, attachments.Attachment]]


class InteractionOption(pydantic.BaseModel):
    name: str
    type: commands.OptionType
    value: typing.Optional[typing.Union[str, int, float]]
    options: typing.Optional[list[InteractionOption]]
    focused: typing.Optional[bool]


class InteractionData(pydantic.BaseModel):
    id: snowflake.Snowflake
    name: str
    type: commands.CommandType
    resolved: typing.Optional[ResolvedData]
    options: typing.Optional[list[InteractionOption]]
    guild_id: typing.Optional[snowflake.Snowflake]
    target_id: typing.Optional[snowflake.Snowflake]


class Interaction(pydantic.BaseModel):
    id: snowflake.Snowflake
    application_id: snowflake.Snowflake
    type: InteractionType
    data: typing.Optional[InteractionData]
    guild_id: typing.Optional[snowflake.Snowflake]
    channel_id: typing.Optional[snowflake.Snowflake]
    member: typing.Optional[members.Member]
    user: typing.Optional[users.User]
    token: str
    version: int
    message: typing.Optional[messages.Message]
    locale: typing.Optional[str]
    guild_locale: typing.Optional[str]


class InteractionCallbackType(enum.IntEnum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9


class InteractionResponse(pydantic.BaseModel):
    type: InteractionCallbackType
    data: typing.Optional[typing.Optional[responses.Message]]
