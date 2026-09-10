"""Async gapipy client. `httpx.AsyncClient(http2=True)` transport by default."""
import inspect
from typing import Optional

import httpx

from .client import _BaseClient, get_config
from .constants import ACCEPTABLE_RESPONSE_STATUS_CODES
from .exceptions import TimeoutError
from .request import _BaseAPIRequestor


class AsyncAPIRequestor(_BaseAPIRequestor):
    """Async mirror of `APIRequestor` — enough for `aget` today."""

    async def _request(self, uri, method, headers=None, timeout=None):
        url = self._get_url(uri)
        request_headers = self._get_headers(method, headers)
        try:
            response = await self.client._httpx.request(
                method, url, headers=request_headers, timeout=timeout,
            )
        except httpx.TimeoutException as exc:
            if timeout:
                raise TimeoutError from exc
            raise

        for callback in self.client._response_callbacks:
            result = callback(response)
            if inspect.isawaitable(result):
                await result

        if response.status_code in ACCEPTABLE_RESPONSE_STATUS_CODES:
            return response.json()
        response.raise_for_status()

    async def get(self, resource_id, variation_id=None, headers=None, timeout=None):
        uri = "/{0}/{1}".format(self._get_uri(), resource_id)
        if variation_id:
            uri = "{0}/{1}".format(uri, variation_id)
        return await self._request(uri, "GET", headers=headers, timeout=timeout)


class AsyncQuery(object):
    """Async mirror of `Query` — currently exposes `aget` only."""

    def __init__(self, client, resource):
        self._client = client
        self.resource = resource

    async def aget(self, resource_id, variation_id=None, headers=None, timeout=None):
        requestor = AsyncAPIRequestor(self._client, self.resource)
        data = await requestor.get(
            resource_id, variation_id=variation_id, headers=headers, timeout=timeout,
        )
        return self.resource(data, client=self._client)


class AsyncClient(_BaseClient):
    """Async gapipy Client. Same seams as sync `Client`; `httpx.AsyncClient` transport."""

    def __init__(self, http2: bool = True, transport: Optional[httpx.AsyncBaseTransport] = None, **config):
        self._load_common_config(config)
        self._init_seams()
        self._httpx = httpx.AsyncClient(http2=http2, transport=transport)
        self._attach_queries(AsyncQuery)

    async def aclose(self):
        await self._httpx.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()
