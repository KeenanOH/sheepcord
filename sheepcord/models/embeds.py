from __future__ import annotations

import datetime
import typing

import pydantic

from sheepcord.models import colors

__all__: typing.Sequence[str] = (
    "EmbedThumbnail",
    "EmbedVideo",
    "EmbedImage",
    "EmbedProvider",
    "EmbedAuthor",
    "EmbedFooter",
    "EmbedField",
    "Embed",
)


class EmbedMediaMixin(pydantic.BaseModel):
    url: str
    proxy_url: typing.Optional[str]
    height: typing.Optional[int]
    width: typing.Optional[int]


class EmbedThumbnail(EmbedMediaMixin):
    pass


class EmbedVideo(EmbedMediaMixin):
    pass


class EmbedImage(EmbedMediaMixin):
    pass


class EmbedProvider(pydantic.BaseModel):
    name: typing.Optional[str]
    url: typing.Optional[str]


class EmbedAuthor(pydantic.BaseModel):
    name: str
    url: typing.Optional[str]
    icon_url: typing.Optional[str]
    proxy_icon_url: typing.Optional[str]


class EmbedFooter(pydantic.BaseModel):
    text: str
    icon_url: typing.Optional[str]
    proxy_icon_url: typing.Optional[str]


class EmbedField(pydantic.BaseModel):
    name: str
    value: str
    inline: typing.Optional[bool]


class Embed(pydantic.BaseModel):
    title: typing.Optional[str]
    type: str = "rich"
    description: typing.Optional[str]
    url: typing.Optional[str]
    timestamp: typing.Optional[datetime.datetime]
    color: typing.Optional[typing.Union[colors.Color, int]]
    footer: typing.Optional[EmbedFooter]
    image: typing.Optional[EmbedImage]
    thumbnail: typing.Optional[EmbedThumbnail]
    video: typing.Optional[EmbedVideo]
    provider: typing.Optional[EmbedProvider]
    author: typing.Optional[EmbedAuthor]
    fields: typing.Optional[list[EmbedField]]

    def set_footer(
        self,
        text: str,
        icon_url: typing.Optional[str] = None,
        proxy_icon_url: typing.Optional[str] = None,
    ) -> Embed:
        self.footer = EmbedFooter(
            text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )
        return self

    def set_image(
        self,
        url: str,
        proxy_url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> Embed:
        self.image = EmbedImage(
            url=url, proxy_url=proxy_url, height=height, width=width
        )
        return self

    def set_thumbnail(
        self,
        url: str,
        proxy_url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> Embed:
        self.thumbnail = EmbedThumbnail(
            url=url, proxy_url=proxy_url, height=height, width=width
        )
        return self

    def set_video(
        self,
        url: str,
        proxy_url: typing.Optional[str] = None,
        height: typing.Optional[int] = None,
        width: typing.Optional[int] = None,
    ) -> Embed:
        self.video = EmbedVideo(
            url=url, proxy_url=proxy_url, height=height, width=width
        )
        return self

    def set_provider(
        self, name: typing.Optional[str] = None, url: typing.Optional[str] = None
    ) -> Embed:
        self.provider = EmbedProvider(name=name, url=url)
        return self

    def set_author(
        self,
        name: str,
        url: typing.Optional[str] = None,
        icon_url: typing.Optional[str] = None,
        proxy_icon_url: typing.Optional[str] = None,
    ) -> Embed:
        self.author = EmbedAuthor(
            name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )
        return self

    def add_field(
        self, name: str, value: str, inline: typing.Optional[bool] = None
    ) -> Embed:
        if not self.fields:
            self.fields = []
        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self
