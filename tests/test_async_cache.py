"""Ticket 08: async cache backends."""
import pytest

from gapipy import AsyncClient
from gapipy.async_cache import (
    AsyncCacheBackend, AsyncNullCache, AsyncRedisCache,
)


async def test_null_cache_is_default_on_async_client():
    async with AsyncClient(application_key="k", http2=False) as ac:
        assert isinstance(ac._cache, AsyncNullCache)


async def test_null_cache_get_returns_none():
    c = AsyncNullCache()
    assert await c.aget("k") is None
    await c.aset("k", "v")
    assert await c.aget("k") is None
    assert await c.ais_cached("k") is False
    assert await c.acount() == 0
    await c.adelete("k")
    await c.aclear()


async def test_custom_async_cache_via_config():
    async with AsyncClient(
        application_key="k", http2=False,
        async_cache_backend="gapipy.async_cache.AsyncNullCache",
    ) as ac:
        assert isinstance(ac._cache, AsyncNullCache)


async def test_async_cache_backend_is_abstract():
    with pytest.raises(TypeError):
        AsyncCacheBackend()


class TestAsyncRedisCache:
    @pytest.fixture
    def redis_client(self):
        import fakeredis.aioredis
        return fakeredis.aioredis.FakeRedis()

    async def test_set_get_roundtrip(self, redis_client):
        c = AsyncRedisCache(client=redis_client)
        await c.aset("k1", {"id": 1, "name": "Peru"})
        assert await c.aget("k1") == {"id": 1, "name": "Peru"}

    async def test_get_missing_returns_none(self, redis_client):
        c = AsyncRedisCache(client=redis_client)
        assert await c.aget("missing") is None

    async def test_is_cached(self, redis_client):
        c = AsyncRedisCache(client=redis_client)
        assert await c.ais_cached("k") is False
        await c.aset("k", "v")
        assert await c.ais_cached("k") is True

    async def test_delete(self, redis_client):
        c = AsyncRedisCache(client=redis_client)
        await c.aset("k", "v")
        await c.adelete("k")
        assert await c.aget("k") is None

    async def test_clear_scoped_by_prefix(self, redis_client):
        a = AsyncRedisCache(client=redis_client, key_prefix="a:")
        b = AsyncRedisCache(client=redis_client, key_prefix="b:")
        await a.aset("x", 1)
        await b.aset("x", 2)
        await a.aclear()
        assert await a.aget("x") is None
        assert await b.aget("x") == 2

    async def test_count(self, redis_client):
        c = AsyncRedisCache(client=redis_client, key_prefix="ctest:")
        assert await c.acount() == 0
        await c.aset("k1", 1)
        await c.aset("k2", 2)
        assert await c.acount() == 2

    async def test_key_prefix_applied(self, redis_client):
        c = AsyncRedisCache(client=redis_client, key_prefix="pfx:")
        await c.aset("k", "v")
        assert await redis_client.get("pfx:k") is not None
        assert await redis_client.get("k") is None
