from __future__ import annotations

import asyncio
import importlib
import pathlib
import typing

import blacksheep
import discord_interactions
import rodi
import uvicorn

from sheepcord import loader
from sheepcord import snowflake, rest
from sheepcord.models import interactions, commands, users, roles, channels, attachments


class Bot:
    def __init__(
        self,
        token: str,
        application_id: str,
        public_key: str,
        register_commands: bool = False,
        debug: bool = False,
    ) -> None:
        self.token: str = token
        self.application_id: str = application_id
        self.public_key: str = public_key
        self._register_commands: bool = register_commands
        self._app: blacksheep.Application = blacksheep.Application(debug=debug)
        self._commands: dict[str, loader.BotCommand] = {}
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._rest: rest.RESTClient = rest.RESTClient(token, application_id)
        self._start_callbacks: list[loader.BotEvent] = []
        self._stop_callbacks: list[loader.BotEvent] = []

        self._app.router.add_post("/", self._handle_request)
        self._app.middlewares.append(self._verify_request)
        self._app.services.add_instance(self)

        self._provider: rodi.Services = self._app.services.build_provider()

    @staticmethod
    def _parse_options(
        interaction: interactions.Interaction,
        options: typing.Union[commands.Option, interactions.InteractionData],
    ) -> dict[
        str,
        typing.Union[
            users.User,
            roles.Role,
            channels.Channel,
            attachments.Attachment,
            commands.Option,
        ],
    ]:
        kwargs: dict[
            str,
            typing.Union[
                users.User,
                roles.Role,
                channels.Channel,
                attachments.Attachment,
                commands.Option,
            ],
        ] = {}

        if options := options.options:
            for option in options:
                if option.type == commands.OptionType.USER:
                    kwargs[option.name] = interaction.data.resolved.users[
                        snowflake.Snowflake(option.value)
                    ]
                elif option.type == commands.OptionType.CHANNEL:
                    kwargs[option.name] = interaction.data.resolved.channels[
                        snowflake.Snowflake(option.value)
                    ]
                elif option.type == commands.OptionType.ROLE:
                    kwargs[option.name] = interaction.data.resolved.roles[
                        snowflake.Snowflake(option.value)
                    ]
                elif option.type == commands.OptionType.MENTIONABLE:
                    if user := interaction.data.resolved.users.get(
                        snowflake.Snowflake(option.value), None
                    ):
                        kwargs[option.name] = user
                    kwargs[option.name] = interaction.data.resolved.roles[
                        snowflake.Snowflake(option.value)
                    ]
                elif option.type == commands.OptionType.ATTACHMENT:
                    kwargs[option.name] = interaction.data.resolved.attachments[
                        snowflake.Snowflake(option.value)
                    ]
                else:
                    kwargs[option.name] = option

        return kwargs

    @staticmethod
    async def _verify_key(request: blacksheep.Request, public_key: str) -> bool:
        return discord_interactions.verify_key(
            await request.read(),
            request.headers.get_first(b"X-Signature-Ed25519").decode(),
            request.headers.get_first(b"X-Signature-Timestamp").decode(),
            public_key,
        )

    def add_dependency_injection_instance(self, instance: typing.Any) -> Bot:
        self._app.services.add_instance(instance)
        self._provider = self._app.services.build_provider()
        return self

    def _get_injected_objects(
        self,
        command_or_event: typing.Union[
            loader.BotCommand, loader.BotEvent, loader.BotSubcommand
        ],
    ) -> dict[str, typing.Any]:
        instances: dict[str, typing.Any] = {}

        if injected_types := command_or_event.inject:
            for key, value in injected_types.items():
                instances[key] = self._provider.get(typing.get_args(value)[0])
        return instances

    async def _handle_deferred_response(
        self,
        interaction: interactions.Interaction,
        bot_command: typing.Union[loader.BotCommand, loader.BotSubcommand],
        **kwargs,
    ) -> None:
        await self._rest.create_followup_message(
            interaction.token, await bot_command.callback(interaction, **kwargs)
        )

    async def _call_bot_command(
        self, interaction: interactions.Interaction, bot_command: loader.BotCommand
    ):
        kwargs = self._parse_options(interaction, interaction.data)
        kwargs.update(self._get_injected_objects(bot_command))

        if bot_command.auto_defer:
            self._loop.create_task(
                self._handle_deferred_response(interaction, bot_command)
            )
            return interactions.InteractionResponse(
                type=interactions.InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            )

        return await bot_command.callback(interaction, **kwargs)

    async def _call_bot_subcommand(
        self,
        interaction: interactions.Interaction,
        bot_subcommand: loader.BotSubcommand,
        options: commands.Option,
    ):
        kwargs = self._parse_options(interaction, options)
        kwargs.update(self._get_injected_objects(bot_subcommand))
        if bot_subcommand.auto_defer:
            self._loop.create_task(
                self._handle_deferred_response(interaction, bot_subcommand)
            )
            return interactions.InteractionResponse(
                type=interactions.InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
            )

        return await bot_subcommand.callback(interaction, **kwargs)

    async def _handle_command(self, interaction: interactions.Interaction):
        if bot_command := self._commands.get(interaction.data.name, None):
            if subcommands := bot_command.subcommands:
                for option in interaction.data.options:
                    if option.name in subcommands.keys():
                        subcommand = subcommands[option.name]
                        return await self._call_bot_subcommand(
                            interaction, subcommand, option
                        )
            return await self._call_bot_command(interaction, bot_command)

    async def _verify_request(
        self, request: blacksheep.Request, handler: typing.Callable
    ):
        if not await self._verify_key(request, self.public_key):
            return blacksheep.Response(204)
        return await handler(request)

    @staticmethod
    async def _handle_request(request: blacksheep.Request, bot: Bot):
        json = await request.json()
        interaction = interactions.Interaction(**json)

        if interaction.type == interactions.InteractionType.PING:
            return blacksheep.json({"type": 1}, 200)
        elif interaction.type == interactions.InteractionType.APPLICATION_COMMAND:
            return await bot._handle_command(interaction)

    async def _register_application_commands(self) -> None:
        for command in self._commands.values():
            await self._rest.register_command(command.command)

    def load_module(self, module: str) -> Bot:
        importlib.import_module(module).loader(self)  # type: ignore
        return self

    def load_modules(self, path: str) -> Bot:
        for path in pathlib.Path(path).glob("*.py"):
            self.load_module(str(path).replace("\\", ".").replace(".py", ""))
        return self

    async def _run_events(self, events: list[loader.BotEvent]) -> None:
        await asyncio.gather(
            *[event.callback(**self._get_injected_objects(event)) for event in events]
        )

    def start(self) -> None:
        if self._register_commands:
            self._loop.run_until_complete(self._register_application_commands())

        self._loop.create_task(self._run_events(self._start_callbacks))
        self._loop.run_until_complete(uvicorn.Server(uvicorn.Config(self._app)).serve())
        self._loop.run_until_complete(self._run_events(self._stop_callbacks))

        for task in asyncio.all_tasks(self._loop):
            task.cancel()

        self._loop.stop()
