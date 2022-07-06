import enum
import typing

import pydantic

from sheepcord import snowflake

__all__: typing.Sequence[str] = ("User", "Flag", "PremiumType")


class Flag(enum.IntFlag):
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19


class PremiumType(enum.IntEnum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class User(pydantic.BaseModel):
    id: snowflake.Snowflake
    username: str
    discriminator: str
    avatar: str
    bot: typing.Optional[bool]
    system: typing.Optional[bool]
    mfa_enabled: typing.Optional[bool]
    banner: typing.Optional[str]
    accent_color: typing.Optional[int]
    locale: typing.Optional[str]
    verified: typing.Optional[bool]
    email: typing.Optional[str]
    public_flags: typing.Optional[Flag]
    flags: typing.Optional[Flag]
    premium_type: typing.Optional[PremiumType]

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"
