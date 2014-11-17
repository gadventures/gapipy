import collections
from functools import partial
from time import time


try:
    import cPickle as pickle
except ImportError:
    import pickle


def make_key(resource_name, resource_id=None):
    if not resource_id:
        return resource_name
    else:
        return '{0}:{1}'.format(resource_name, resource_id)


def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def _items(mappingorseq):
    """Wrapper for efficient iteraiton over mappings represeted by dicts or
    sequeunces::

        >>> for k, v in _items([i, i*i] for i in xrange(5)):
        ...     assert k*k == v

        >>> for k, v in _items({i: i*i} for i in xrange(5)):
        ...     assert k*k == v
    """
    return mappingorseq.iteritems() if hasattr(mappingorseq, 'iteritems') \
        else mappingorseq


class BaseCache(object):
    """Base class for the cache system. All the cache systems will implemtent
    this API or a superset of it.

    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`set`.
    """

    def __init__(self, default_timeout=300, **kwargs):
        self.default_timeout = default_timeout

    def get(self, resource_name, resource_id=None):
        return None

    def set(self, resource_name, data_dict):
        pass

    def set_many(self, resource_name, sequence, timeout=None):
        for data_dict in sequence:
            self.set(resource_name, data_dict, timeout)

    def get_many(self, resource_name, ids):
        func = partial(self.get, resource_name)
        return map(func, ids)

    def delete(self, resource_name, resource_id=None):
        pass

    def clear(self):
        pass

    def count(self):
        raise NotImplementedError

    def is_cached(self, resource_id):
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
        BaseCache.__init__(self, default_timeout)
        self._cache = {}
        self._threshold = threshold

    def _prune(self):
        if len(self._cache) > self._threshold:
            now = time()
            # Prune expired keys, or every few keys.
            for idx, (key, (expires, _)) in enumerate(self._cache.items()):
                if expires <= now or idx % 3 == 0:
                    self._cache.pop(key, None)

    def get(self, resource_name, resource_id=None):
        key = make_key(resource_name, resource_id)
        expires, value = self._cache.get(key, (0, None))
        if expires > time():
            return pickle.loads(value)

    def set(self, resource_name, data_dict, timeout=None):
        key = make_key(resource_name, data_dict.get('id'))
        if timeout is None:
            timeout = self.default_timeout
        self._prune()

        self._cache[key] = (time() + timeout, pickle.dumps(data_dict,
                            pickle.HIGHEST_PROTOCOL))

    def delete(self, resource_name, resource_id=None):
        key = make_key(resource_name, resource_id)
        return self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()

    def count(self):
        return len(self._cache)

    def is_cached(self, resource_name, resource_id):
        key = make_key(resource_name, resource_id)
        return key in self._cache


class RedisCache(BaseCache):
    """Uses the Redis key-value store as a cache backend.
    """
    def __init__(self, host='localhost', port=6379, password=None,
                 db=0, default_timeout=300, key_prefix=None, **kwargs):
        BaseCache.__init__(self, default_timeout)
        self.key_prefix = key_prefix or ''
        try:
            import redis
        except ImportError:
            raise RuntimeError('no redis module found')
        self._client = redis.Redis(host=host, port=port, password=password, db=db)

    def load_object(self, value):
        """The reversal of `dump_object`. This might be called with None.
        """
        if value is None:
            return None
        return pickle.loads(value)

    def dump_object(self, value):
        return pickle.dumps(value)

    def get(self, resource_name, resource_id=None):
        key = make_key(resource_name, resource_id)
        return self.load_object(self._client.get(self.key_prefix + key))

    def set(self, resource_name, data_dict, timeout=None):
        key = make_key(resource_name, data_dict.get('id', None))
        if timeout is None:
            timeout = self.default_timeout
        data = self.dump_object(data_dict)
        return self._client.setex(self.key_prefix + key, data, timeout)

    def delete(self, resource_name, resource_id=None):
        key = make_key(resource_name, resource_id)
        return self._client.delete(self.key_prefix + key)

    def clear(self):
        cache_keys = self._client.keys('{}*'.format(self.key_prefix))
        map(self._client.delete, cache_keys)

    def info(self):
        return self._client.info()

    def is_cached(self, resource_name, resource_id):
        key = make_key(resource_name, resource_id)
        return self._client.exists(self.key_prefix + key)
