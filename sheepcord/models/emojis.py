import typing

import pydantic

from sheepcord import snowflake
from sheepcord.models import users

__all__: typing.Sequence[str] = ("Emoji",)


class Emoji(pydantic.BaseModel):
    id: typing.Optional[snowflake.Snowflake]
    name: typing.Optional[str]
    roles: typing.Optional[snowflake.Snowflake]
    user: typing.Optional[users.User]
    require_colons: typing.Optional[bool]
    managed: typing.Optional[bool]
    animated: typing.Optional[bool]
    available: typing.Optional[bool]
