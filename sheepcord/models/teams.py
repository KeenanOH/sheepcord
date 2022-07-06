import enum
import typing

import pydantic

from sheepcord import snowflake
from sheepcord.models import users

__all__: typing.Sequence[str] = ("MembershipState", "TeamMember", "Team")


class MembershipState(enum.IntEnum):
    INVITED = 1
    ACCEPTED = 2


class TeamMember(pydantic.BaseModel):
    membership_state: MembershipState
    permissions: list[str]
    team_id: snowflake.Snowflake
    user: users.User


class Team(pydantic.BaseModel):
    icon: typing.Optional[str]
    id: snowflake.Snowflake
    members: list[TeamMember]
    name: str
    owner_user_id: snowflake.Snowflake
