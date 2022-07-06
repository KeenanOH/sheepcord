import enum
import typing

import pydantic

from sheepcord import snowflake
from sheepcord.models import users

__all__: typing.Sequence[str] = (
    "StickerFormatType",
    "StickerItem",
    "StickerType",
    "Sticker",
)


class StickerFormatType(enum.IntEnum):
    PNG = 1
    APNG = 2
    LOTTIE = 3


class StickerItem(pydantic.BaseModel):
    id: snowflake.Snowflake
    name: str
    format_type: StickerFormatType


class StickerType(enum.IntEnum):
    STANDARD = 1
    GUILD = 2


class Sticker(pydantic.BaseModel):
    id: snowflake.Snowflake
    pack_id: typing.Optional[snowflake.Snowflake]
    name: str
    description: str
    tags: str
    type: StickerType
    format_type: StickerFormatType
    available: typing.Optional[bool]
    guild_id: typing.Optional[snowflake.Snowflake]
    user: typing.Optional[users.User]
    sort_value: typing.Optional[int]
