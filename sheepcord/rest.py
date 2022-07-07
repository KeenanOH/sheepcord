import typing

import blacksheep
import pydantic
from blacksheep import client

from sheepcord import exceptions
from sheepcord.models import commands, interactions

__all__: typing.Sequence[str] = ("RESTClient",)


class RESTClient:
    def __init__(
        self,
        token: str,
        application_id: str,
    ) -> None:
        self._http_client: typing.Optional[client.ClientSession] = None
        self.token: str = token
        self.application_id: str = application_id
        self._headers: list[tuple[bytes, bytes]] = [
            (b"Authorization", f"Bot {self.token}".encode())
        ]
        self._retry_after: int = 0

    async def _handle_request(
        self,
        method: str,
        url: str,
        content: typing.Optional[blacksheep.JSONContent] = None,
        parse_into: typing.Optional[typing.Type] = None,
    ):
        if not self._http_client:
            self._http_client = client.ClientSession(
                base_url="https://discord.com/api/v10", default_headers=self._headers
            )

        request: blacksheep.Request = blacksheep.Request(
            method, self._http_client.get_url(url), None
        )

        response: blacksheep.Response = await self._http_client.send(
            request.with_content(content) if content else request
        )

        if response.status - 200 >= 100:
            raise exceptions.RESTException(
                f"{response.status}: {await response.text()}"
            )

        if model := parse_into:
            return pydantic.parse_obj_as(model, await response.json())

    async def register_command(self, command: commands.Command) -> None:
        print(command.name)
        await self._handle_request(
            "POST",
            f"/applications/{self.application_id}/commands",
            blacksheep.JSONContent(command),
        )

    async def create_followup_message(
        self,
        interaction_token: str,
        response: interactions.InteractionResponse,
    ):
        await self._handle_request(
            "POST",
            f"/webhooks/{self.application_id}/{interaction_token}",
            blacksheep.JSONContent(response),
        )

    async def close(self) -> None:
        await self._http_client.close()
