import typing

import pydantic

from sheepcord import snowflake, permissions
from sheepcord.models import colors

__all__: typing.Sequence[str] = ("RoleTag", "Role")


class RoleTag(pydantic.BaseModel):
    bot_id: snowflake.Snowflake
    integration_id: snowflake.Snowflake
    premium_subscriber: None


class Role(pydantic.BaseModel):
    id: snowflake.Snowflake
    name: str
    color: colors.Color
    hoist: bool
    icon: typing.Optional[str]
    unicode_emoji: typing.Optional[str]
    position: int
    permissions: permissions.Permissions
    managed: bool
    mentionable: bool
    tags: typing.Optional[RoleTag]
