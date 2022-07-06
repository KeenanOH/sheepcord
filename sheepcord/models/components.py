from __future__ import annotations

import enum
import typing

import pydantic

from sheepcord.models import emojis

__all__: typing.Sequence[str] = (
    "ComponentType",
    "ButtonStyle",
    "Button",
    "SelectOption",
    "SelectMenu",
    "TextInputStyle",
    "TextInput",
    "ActionRow",
)


class ComponentType(enum.IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    SELECT_MENU = 3
    TEXT_INPUT = 4


class ButtonStyle(enum.IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class Button(pydantic.BaseModel):
    type: ComponentType = ComponentType.BUTTON
    style: ButtonStyle
    label: typing.Optional[str]
    emoji: emojis.Emoji
    custom_id: typing.Optional[str]
    url: typing.Optional[str]
    disabled: typing.Optional[str]


class SelectOption(pydantic.BaseModel):
    label: str
    value: str
    description: typing.Optional[str]
    emoji: typing.Optional[emojis.Emoji]
    default: typing.Optional[bool]


class SelectMenu(pydantic.BaseModel):
    type: ComponentType = ComponentType.SELECT_MENU
    custom_id: str
    options: typing.Optional[list[SelectOption]]
    placeholder: typing.Optional[str]
    min_values: typing.Optional[str]
    max_values: typing.Optional[int]
    disabled: typing.Optional[bool]

    def add_option(
        self,
        label: str,
        value: str,
        description: typing.Optional[str] = None,
        emoji: typing.Optional[emojis.Emoji] = None,
        default: typing.Optional[bool] = None,
    ) -> SelectMenu:
        if not self.options:
            self.options = []
        self.options.append(
            SelectOption(
                label=label,
                value=value,
                description=description,
                emoji=emoji,
                default=default,
            )
        )
        return self


class TextInputStyle(enum.IntEnum):
    SHORT = 1
    PARAGRAPH = 2


class TextInput(pydantic.BaseModel):
    type: ComponentType = ComponentType.TEXT_INPUT
    custom_id: str
    style: TextInputStyle
    label: str
    min_length: typing.Optional[int]
    max_length: typing.Optional[int]
    required: typing.Optional[bool]
    value: typing.Optional[str]
    placeholder: typing.Optional[str]


class ActionRow(pydantic.BaseModel):
    type: ComponentType = ComponentType.ACTION_ROW
    components: typing.Optional[list[typing.Union[Button, SelectMenu, TextInput]]]

    def add_component(
        self, component: typing.Union[Button, SelectMenu, TextInput]
    ) -> ActionRow:
        if not self.components:
            self.components = []
        self.components.append(component)
        return self
