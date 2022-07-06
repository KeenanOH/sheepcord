from __future__ import annotations

import asyncio
import importlib
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
        self._start_callbacks: list[typing.Callable] = []
        self._stop_callbacks: list[typing.Callable] = []

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

    async def _call_bot_command(
        self, interaction: interactions.Interaction, bot_command: loader.BotCommand
    ):
        kwargs = {}

        if injected_types := bot_command.inject:
            for key, value in injected_types.items():
                kwargs[key] = self._provider.get(typing.get_args(value)[0])

        kwargs.update(self._parse_options(interaction, interaction.data))

        return await bot_command.callback(interaction, **kwargs)

    async def _handle_command(self, interaction: interactions.Interaction):
        if bot_command := self._commands.get(interaction.data.name, None):
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
            print(command.command.dict(exclude_none=True))
            await self._rest.register_command(command.command)

    def load_module(self, module: str) -> Bot:
        importlib.import_module(module).loader(self)
        return self

    async def _gather(self, callbacks: list[typing.Callable]) -> None:
        await asyncio.gather(*[callback() for callback in callbacks])

    def start(self):
        if self._register_commands:
            self._start_callbacks.append(self._register_application_commands)

        self._loop.create_task(self._gather(self._start_callbacks))

        server: uvicorn.Server = uvicorn.Server(uvicorn.Config(self._app))
        self._loop.run_until_complete(server.serve())

        self._loop.run_until_complete(self._gather(self._stop_callbacks))

        for task in asyncio.all_tasks(self._loop):
            task.cancel()

        self._loop.stop()
