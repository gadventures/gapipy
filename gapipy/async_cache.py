"""Async cache backends for `AsyncClient`.

`AsyncCacheBackend` is the ABC; every method mirrors the sync `BaseCache` API
with an `a` prefix. `AsyncNullCache` is the default when no backend is
configured. `AsyncRedisCache` uses `redis.asyncio` — no thread-pool wrapping.
"""
# pickle is safe here: values in the Redis cache come only from this process's
# own `aset` calls (JSON payloads returned by GAPI). Same posture as the sync
# `gapipy.cache.RedisCache`.
import pickle
from abc import ABC, abstractmethod


class AsyncCacheBackend(ABC):
    """Async cache interface. Mirrors `gapipy.cache.BaseCache` method-for-method."""

    def __init__(self, default_timeout=300, **kwargs):
        self.default_timeout = default_timeout

    @abstractmethod
    async def aget(self, key): ...

    @abstractmethod
    async def aset(self, key, value, timeout=None): ...

    @abstractmethod
    async def adelete(self, key): ...

    @abstractmethod
    async def aclear(self): ...

    @abstractmethod
    async def acount(self): ...

    @abstractmethod
    async def ais_cached(self, key): ...


class AsyncNullCache(AsyncCacheBackend):
    """No-op cache. Default for `AsyncClient` when nothing else is configured."""

    async def aget(self, key):
        return None

    async def aset(self, key, value, timeout=None):
        return None

    async def adelete(self, key):
        return None

    async def aclear(self):
        return None

    async def acount(self):
        return 0

    async def ais_cached(self, key):
        return False


class AsyncRedisCache(AsyncCacheBackend):
    """Async Redis-backed cache. Uses `redis.asyncio`."""

    def __init__(self, host="localhost", port=6379, password=None, db=0,
                 default_timeout=300, key_prefix="", client=None, **kwargs):
        super().__init__(default_timeout=default_timeout, **kwargs)
        self.key_prefix = key_prefix
        if client is not None:
            self._client = client
        else:
            try:
                from redis import asyncio as aioredis
            except ImportError as exc:
                raise RuntimeError("redis>=5.0 required for AsyncRedisCache") from exc
            self._client = aioredis.Redis(host=host, port=port, password=password, db=db)

    def _k(self, key):
        return self.key_prefix + key

    async def aget(self, key):
        raw = await self._client.get(self._k(key))
        if raw is None:
            return None
        return pickle.loads(raw)

    async def aset(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        return await self._client.set(self._k(key), pickle.dumps(value), ex=timeout)

    async def adelete(self, key):
        return await self._client.delete(self._k(key))

    async def aclear(self):
        keys = await self._client.keys("{}*".format(self.key_prefix))
        if keys:
            await self._client.delete(*keys)

    async def acount(self):
        return len(await self._client.keys("{}*".format(self.key_prefix)))

    async def ais_cached(self, key):
        return bool(await self._client.exists(self._k(key)))
