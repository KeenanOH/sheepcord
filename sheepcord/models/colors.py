from __future__ import annotations

import typing

__all__: typing.Sequence[str] = ("Color",)


class Color(int):
    DEFAULT: int = 0
    TEAL: int = 0x1ABC9C
    DARK_TEAL: int = 0x11806A
    GREEN: int = 0x2ECC71
    DARK_GREEN: int = 0x1F8B4C
    BLUE: int = 0x3498DB
    DARK_BLUE: int = 0x206694
    PURPLE: int = 0x9B59B6
    DARK_PURPLE: int = 0x71368A
    MAGENTA: int = 0xE91E63
    DARK_MAGENTA = 0xAD1457
    GOLD: int = 0xF1C40F
    DARK_GOLD: int = 0xC27C0E
    ORANGE: int = 0xE67E22
    DARK_ORANGE: int = 0xA84300
    RED: int = 0xE74C3C
    DARK_RED: int = 0x992D22
    LIGHTER_GREY: int = 0x95A5A6
    DARK_GREY: int = 0x607D8B
    LIGHT_GREY: int = 0x979C9F
    DARKER_GREY: int = 0x546E7A
    BLURPLE: int = 0x7289DA
    GREYPLE: int = 0x99AAB5
