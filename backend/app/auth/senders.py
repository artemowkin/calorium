from aiohttp import client

from ..project.settings import settings
from .exceptions import MessageNotSended


class EmailSender:

    def __init__(self, api_url: str = settings.email_service_url,
                 endpoint: str = '/v1/email/messages',
                 api_key: str = settings.email_service_api_key,
                 sender: str = settings.email_service_sender):
        self._api_url = api_url
        self._endpoint = endpoint
        self._api_key = api_key
        self._sender = sender

    async def send_email(self, address: str, text: str) -> None:
        headers = {"Authorization": f"Bearer {self._api_key}"}
        async with client.ClientSession(self._api_url, headers=headers) as session:
            body = {
                'from_email': self._sender,
                'to': address,
                'subject': 'Код верификации',
                'html': text,
            }
            async with session.post(self._endpoint, json=body) as response:
                if not response.ok:
                    response_json = await response.json()
                    print(response_json)
                    raise MessageNotSended(response_json)

