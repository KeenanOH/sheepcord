import datetime
import typing

import pydantic

from sheepcord import snowflake, permissions
from sheepcord.models import users

__all__: typing.Sequence[str] = ("Member",)


class Member(pydantic.BaseModel):
    user: typing.Optional[users.User]
    nick: typing.Optional[str]
    avatar: typing.Optional[str]
    roles: list[snowflake.Snowflake]
    joined_at: datetime.datetime
    premium_since: typing.Optional[datetime.datetime]
    deaf: typing.Optional[bool]
    mute: typing.Optional[bool]
    pending: typing.Optional[bool]
    permissions: typing.Union[int, permissions.Permissions]  # TODO: fix permissions
    communication_disabled_until: typing.Optional[datetime.datetime]
