import typing

import pydantic

from sheepcord import snowflake

__all__: typing.Sequence[str] = ("Attachment",)


class Attachment(pydantic.BaseModel):
    id: snowflake.Snowflake
    filename: str
    description: typing.Optional[str]
    content_type: typing.Optional[str]
    size: int
    url: str
    proxy_url: str
    height: typing.Optional[int]
    width: typing.Optional[int]
    ephemeral: typing.Optional[bool]
