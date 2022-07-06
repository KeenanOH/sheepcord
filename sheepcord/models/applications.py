import enum
import typing

import pydantic

from sheepcord import snowflake, permissions
from sheepcord.models import users, teams

__all__: typing.Sequence[str] = (
    "ApplicationFlags",
    "InstallParams",
    "Application",
)


class ApplicationFlags(enum.IntEnum):
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19


class InstallParams(pydantic.BaseModel):
    scopes: list[str]
    permissions: permissions.Permissions


class Application(pydantic.BaseModel):
    id: snowflake.Snowflake
    name: str
    icon: str
    description: str
    rpc_origins: typing.Optional[str]
    bot_public: bool
    bot_require_code_grant: bool
    terms_of_service_url: typing.Optional[str]
    privacy_policy_url: typing.Optional[str]
    owner: typing.Optional[users.User]
    verify_key: str
    team: teams.Team
    guild_id: typing.Optional[snowflake.Snowflake]
    primary_sku_id: typing.Optional[snowflake.Snowflake]
    slug: typing.Optional[str]
    cover_image: typing.Optional[str]
    flags: typing.Optional[ApplicationFlags]
    tags: typing.Optional[list[str]]
    install_params: typing.Optional[InstallParams]
    custom_install_url: typing.Optional[str]
