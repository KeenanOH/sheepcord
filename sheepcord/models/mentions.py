import typing

import pydantic

from sheepcord import snowflake

__all__: typing.Sequence[str] = ("AllowedMentions",)


class AllowedMentions(pydantic.BaseModel):
    parse: list[typing.Literal["roles", "users", "everyone"]]
    roles: list[snowflake.Snowflake]
    users: list[snowflake.Snowflake]
    replied_user: bool
