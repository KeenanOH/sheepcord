from __future__ import annotations

import enum
import typing

import pydantic

from sheepcord import permissions
from sheepcord.models import channels

__all__: typing.Sequence[str] = (
    "CommandType",
    "OptionType",
    "Choice",
    "Option",
    "Command",
)


class CommandType(enum.IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class OptionType(enum.IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class Choice(pydantic.BaseModel):
    name: str
    value: typing.Union[str, int, float]


class Option(pydantic.BaseModel):
    type: OptionType
    name: str
    description: str
    required: typing.Optional[bool]
    choices: typing.Optional[list[Choice]]
    options: typing.Optional[list[Option]]
    channel_types: typing.Optional[list[channels.ChannelType]]
    min_value: typing.Optional[typing.Union[int, float]]
    max_value: typing.Optional[typing.Union[int, float]]
    autocomplete: typing.Optional[bool]


class Command(pydantic.BaseModel):
    name: str
    description: str
    options: typing.Optional[list[Option]]
    default_member_permissions: permissions.Permissions
    dm_permissions: typing.Optional[bool]
    type: typing.Optional[CommandType]

    def add_option(self, option: Option) -> Command:
        if not self.options:
            self.options = []
        self.options.append(option)
        return self
