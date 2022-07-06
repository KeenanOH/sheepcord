import typing

import pydantic

from sheepcord.models import emojis

__all__: typing.Sequence[str] = ("Reaction",)


class Reaction(pydantic.BaseModel):
    count: int
    me: bool
    emoji: emojis.Emoji
