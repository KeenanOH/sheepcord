from __future__ import annotations

import dataclasses
import enum
import inspect
import typing

from sheepcord import permissions, bot
from sheepcord.models import commands, channels

__all__: typing.Sequence[str] = (
    "command",
    "option",
    "Loader",
    "Inject",
    "event",
    "BotEventType",
    "BotCommand"
)

T = typing.TypeVar("T")
Inject = typing.Annotated[T, typing.Any]


@dataclasses.dataclass
class BotSubcommand:
    callback: typing.Callable
    command: commands.Option
    auto_defer: bool
    inject: typing.Optional[dict[str, typing.Type]] = None


@dataclasses.dataclass
class BotCommand:
    command: commands.Command
    auto_defer: bool
    callback: typing.Optional[typing.Callable] = None
    subcommands: typing.Optional[dict[str, BotSubcommand]] = None
    subcommand_groups: typing.Optional[dict[str, list[BotSubcommand]]] = None
    inject: typing.Optional[dict[str, typing.Type]] = None

    def subcommand(self, name: str, description: str, auto_defer: bool = False):
        def inner(callback: typing.Callable):
            if not self.subcommands:
                self.subcommands = {}
            subcommand: BotSubcommand = BotSubcommand(
                callback,
                commands.Option(
                    type=commands.OptionType.SUB_COMMAND,
                    name=name,
                    description=description,
                ),
                auto_defer,
            )
            _inspect_signature(subcommand)
            self.subcommands[name] = subcommand
            return subcommand

        return inner


@dataclasses.dataclass
class BotOption:
    callback: typing.Callable
    option: commands.Option
    options: list[BotOption]


class BotEventType(enum.IntEnum):
    START = 1
    STOP = 2


@dataclasses.dataclass
class BotEvent:
    callback: typing.Callable
    type: BotEventType
    inject: typing.Optional[dict[str, typing.Type]] = None


def _inspect_signature(
    command_or_event: typing.Union[BotCommand, BotEvent, BotSubcommand]
) -> None:
    signature: inspect.Signature = inspect.signature(command_or_event.callback)
    for parameter in signature.parameters.values():
        if "sheepcord.loader.Inject" in str(parameter.annotation):
            if not command_or_event.inject:
                command_or_event.inject = {}
            command_or_event.inject[parameter.name] = parameter.annotation


def command(
    name: str,
    description: str,
    default_member_permissions: permissions.Permissions = permissions.Permissions.USE_APPLICATION_COMMANDS,
    dm_permissions: typing.Optional[bool] = None,
    auto_defer: bool = False,
    type: typing.Optional[commands.CommandType] = None,
):
    def inner(callback: typing.Union[typing.Callable, BotOption]) -> BotCommand:
        if isinstance(callback, BotOption):
            options = [x.option for x in callback.options]
            callback = callback.callback
        else:
            options = []
        bot_command: BotCommand = BotCommand(
            callback,
            commands.Command(
                name=name,
                description=description,
                options=options,
                default_member_permissions=default_member_permissions,
                dm_permissions=dm_permissions,
                type=type,
            ),
            auto_defer,
        )
        _inspect_signature(bot_command)
        return bot_command

    return inner


def option(
    type: commands.OptionType,
    name: str,
    description: str,
    required: typing.Optional[bool] = None,
    choices: typing.Optional[list[commands.Choice]] = None,
    channel_types: typing.Optional[list[channels.ChannelType]] = None,
    min_value: typing.Optional[typing.Union[int, float]] = None,
    max_value: typing.Optional[typing.Union[int, float]] = None,
    autocomplete: typing.Optional[bool] = None,
):
    def inner(callback: typing.Union[typing.Callable, BotOption]) -> BotOption:
        if isinstance(callback, BotOption):
            options = callback.options
            callback = callback.callback
        else:
            options = []

        option = BotOption(
            callback,
            commands.Option(
                type=type,
                name=name,
                description=description,
                required=required,
                choices=choices,
                channel_types=channel_types,
                min_value=min_value,
                max_value=max_value,
                autocomplete=autocomplete,
            ),
            options,
        )
        option.options = [option] + option.options
        return option

    return inner


def event(type: BotEventType):
    def inner(callback: typing.Callable):
        event: BotEvent = BotEvent(callback, type)
        _inspect_signature(event)
        return event

    return inner


class Loader:
    def __init__(self, locals: dict[str, typing.Any]):
        self.locals = locals

    def __call__(self, bot: bot.Bot) -> None:
        for local in self.locals.values():
            if isinstance(local, BotCommand):
                if subcommands := local.subcommands:
                    for subcommand in subcommands.values():
                        local.command.add_option(subcommand.command)
                bot._commands[local.command.name] = local
            elif isinstance(local, BotEvent):
                if local.type == BotEventType.START:
                    bot._start_callbacks.append(local)
                else:
                    bot._stop_callbacks.append(local)
