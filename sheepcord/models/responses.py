import typing

import pydantic

from sheepcord.models import embeds, mentions, components, attachments, commands

__all__: typing.Sequence[str] = ("Message", "Autocomplete", "Modal", "DeferredResponse")


class Message(pydantic.BaseModel):
    tts: typing.Optional[bool]
    content: typing.Optional[str]
    embeds: typing.Optional[list[embeds.Embed]]
    allowed_mentions: typing.Optional[mentions.AllowedMentions]
    flags: typing.Optional[int]
    components: typing.Optional[
        typing.Union[
            components.ActionRow,
            components.Button,
            components.SelectMenu,
            components.TextInput,
        ]
    ]
    attachments: typing.Optional[list[attachments.Attachment]]


class Autocomplete(pydantic.BaseModel):
    choices: list[commands.Choice]


class Modal(pydantic.BaseModel):
    custom_id: str
    title: str
    components: list[components.TextInput]


class DeferredResponse(pydantic.BaseModel):
    content: typing.Optional[str]
    embeds: typing.Optional[list[embeds.Embed]]
    allowed_mentions: typing.Optional[mentions.AllowedMentions]
    components: typing.Optional[
        typing.Union[
            components.ActionRow,
            components.Button,
            components.TextInput,
            components.SelectMenu,
        ]
    ]
    attachments: typing.Optional[attachments.Attachment]
