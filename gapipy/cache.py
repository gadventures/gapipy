from time import time


try:
    import cPickle as pickle
except ImportError:
    import pickle


class BaseCache(object):
    """Base class for the cache system. All the cache systems will implement
    this API or a superset of it.

    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`set`.
    """
    def __init__(self, default_timeout=300, **kwargs):
        self.default_timeout = default_timeout

    def get(self, key):
        return None

    def set(self, key, value):
        pass

    def delete(self, key):
        pass

    def clear(self):
        pass

    def count(self):
        raise NotImplementedError

    def is_cached(self, key):
        return False


class NullCache(BaseCache):
    """
    A cache that doesn't cache.
    """


class SimpleCache(BaseCache):
    """Simply memory cache for single process environments. This class exists
    mainly for a development server and is not 100% thread safe.

    :param threshold: the maximum number of items the cache stores before
                      it starts evicting keys.
    """
    def __init__(self, threshold=500, default_timeout=300, **kwargs):
        super(SimpleCache, self).__init__(default_timeout, **kwargs)
        self._cache = {}
        self.threshold = threshold

    def _prune(self):
        if len(self._cache) > self.threshold:
            now = time()
            # Prune expired keys, or every few keys.
            for idx, (key, (expires, _)) in enumerate(self._cache.items()):
                if expires <= now or idx % 3 == 0:
                    self._cache.pop(key, None)

    def get(self, key):
        expires, value = self._cache.get(key, (0, None))
        if expires > time():
            return pickle.loads(value)

    def set(self, key, data_dict, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        self._prune()
        self._cache[key] = (time() + timeout, pickle.dumps(data_dict,
                            pickle.HIGHEST_PROTOCOL))

    def delete(self, key):
        return self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()

    def count(self):
        return len(self._cache)

    def is_cached(self, key):
        return key in self._cache


class RedisCache(BaseCache):
    """Uses the Redis key-value store as a cache backend."""

    _connection_pool_cache = {}

    def __init__(self, host='localhost', port=6379, password=None,
                 db=0, default_timeout=300, key_prefix='', **kwargs):
        super(RedisCache, self).__init__(default_timeout, **kwargs)
        self.key_prefix = key_prefix
        self._client = self._get_client(host, port, password, db)

    @classmethod
    def _get_client(cls, host, port, password, db):
        """
        Retrieves a connection pool from a class-local cache (or creates it if
        necessary), returns a Redis client instance that uses that pool.
        """
        try:
            import redis
        except ImportError:
            raise RuntimeError('no redis module found')
        credentials = (host, port, password, db)
        pool = cls._connection_pool_cache.get(
            credentials,
            redis.ConnectionPool(host=host, port=port, password=password, db=db))
        cls._connection_pool_cache[credentials] = pool
        return redis.Redis(connection_pool=pool)

    def load_object(self, value):
        """The reversal of `dump_object`. This might be called with `None`."""
        if value is None:
            return None
        return pickle.loads(value)

    def dump_object(self, value):
        return pickle.dumps(value)

    def get(self, key):
        return self.load_object(self._client.get(self.key_prefix + key))

    def set(self, key, data_dict, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        data = self.dump_object(data_dict)
        return self._client.setex(self.key_prefix + key, data, timeout)

    def delete(self, key):
        return self._client.delete(self.key_prefix + key)

    def clear(self):
        cache_keys = self._client.keys('{}*'.format(self.key_prefix))
        map(self._client.delete, cache_keys)

    def info(self):
        return self._client.info()

    def is_cached(self, key):
        return self._client.exists(self.key_prefix + key)
