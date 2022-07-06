import typing

__all__: typing.Sequence[str] = ("SheepcordException", "RESTException")


class SheepcordException(Exception):
    pass


class RESTException(Exception):
    pass
