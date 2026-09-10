"""Async gapipy client. `httpx.AsyncClient(http2=True)` transport by default."""
import inspect
from copy import deepcopy
from importlib import import_module
from typing import Optional
from urllib.parse import urlparse

import httpx

from .client import _BaseClient, get_config
from .constants import ACCEPTABLE_RESPONSE_STATUS_CODES
from .exceptions import TimeoutError
from .request import _BaseAPIRequestor


class AsyncAPIRequestor(_BaseAPIRequestor):
    """Async mirror of `APIRequestor`. Provides `get`, `list_raw`, `list`."""

    async def _request(self, uri, method, params=None, headers=None, timeout=None):
        url = self._get_url(uri)
        request_headers = self._get_headers(method, headers)
        try:
            response = await self.client._httpx.request(
                method, url, params=params, headers=request_headers, timeout=timeout,
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

    async def list_raw(self, uri=None):
        """Async twin of `APIRequestor.list_raw`. One page only."""
        if uri:
            if urlparse(uri).query:
                return await self._request(uri, "GET")
            return await self._request(uri, "GET", params=self.params)

        if self.parent:
            parts = [
                self.parent.uri,
                self.parent.id,
                self.parent.variation_id,
                self._get_uri(),
            ]
            uri = "/{0}".format("/".join(filter(None, parts)))
        else:
            uri = "/{0}".format(self._get_uri())
        return await self._request(uri, "GET", params=self.params)

    async def list(self, uri=None):
        """Async generator walking every page via `next` links."""
        response = await self.list_raw(uri)
        for result in response["results"]:
            yield result

        for link in response.get("links", []):
            if link["rel"] != "next":
                continue
            async for result in self.list(link["href"]):
                yield result


class AsyncQuery(object):
    """Async mirror of `Query`. Supports `aget`, `filter`, `__aiter__`, `all`."""

    def __init__(self, client, resource, filters=None, parent=None, raw_data=None):
        self._client = client
        self.resource = resource
        self.parent = parent
        self._filters = filters or {}
        self._raw_data = raw_data or {}

    def _clone(self):
        return AsyncQuery(
            self._client,
            self.resource,
            filters=deepcopy(self._filters),
            parent=self.parent,
            raw_data=deepcopy(self._raw_data),
        )

    def filter(self, **kwargs):
        """Return a new AsyncQuery with the given filters merged in."""
        clone = self._clone()
        clone._filters.update(kwargs)
        return clone

    async def aget(self, resource_id, variation_id=None, headers=None, timeout=None):
        requestor = AsyncAPIRequestor(self._client, self.resource)
        data = await requestor.get(
            resource_id, variation_id=variation_id, headers=headers, timeout=timeout,
        )
        return self.resource(data, client=self._client)

    def __aiter__(self):
        return self.all()

    async def afirst(self):
        """First result or None."""
        async for item in self.all(limit=1):
            return item
        return None

    async def acount(self):
        """Total count reported by GAPI on the first list page."""
        requestor = AsyncAPIRequestor(
            self._client, self.resource, params=self._filters, parent=self.parent,
        )
        page = await requestor.list_raw()
        return page.get("count")

    async def aexists(self):
        """True if the query has at least one result. Short-circuits after first page."""
        requestor = AsyncAPIRequestor(
            self._client, self.resource, params=self._filters, parent=self.parent,
        )
        page = await requestor.list_raw()
        return bool(page.get("results"))

    async def alist(self, limit=None):
        """Materialize the async generator into a list."""
        return [item async for item in self.all(limit=limit)]

    async def all(self, limit=None):
        """Async generator hydrating every record across every page."""
        if limit is not None:
            if not isinstance(limit, int):
                raise TypeError("limit must be an integer")
            if limit <= 0:
                raise ValueError("limit must be a positive integer")

        requestor = AsyncAPIRequestor(
            self._client, self.resource, params=self._filters, parent=self.parent,
        )
        href = self._raw_data.get("href") if isinstance(self._raw_data, dict) else None
        yielded = 0
        async for result in requestor.list(href):
            yield self.resource(result, client=self._client, stub=True)
            yielded += 1
            if limit is not None and yielded >= limit:
                return


class AsyncClient(_BaseClient):
    """Async gapipy Client. Same seams as sync `Client`; `httpx.AsyncClient` transport."""

    def __init__(self, http2: bool = True, transport: Optional[httpx.AsyncBaseTransport] = None, **config):
        self._load_common_config(config)
        self._init_seams()
        self._httpx = httpx.AsyncClient(http2=http2, transport=transport)
        self._set_cache_instance(
            get_config(config, 'async_cache_backend'),
            get_config(config, 'cache_options'),
        )
        self._attach_queries(AsyncQuery)

    def _set_cache_instance(self, backend_path, cache_options):
        module_name, class_name = backend_path.rsplit('.', 1)
        cache_cls = getattr(import_module(module_name), class_name)
        self._cache = cache_cls(**cache_options)

    async def aclose(self):
        await self._httpx.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()
