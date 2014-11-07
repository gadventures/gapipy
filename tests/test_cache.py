import time
from unittest import TestCase, skipUnless

from gapipy import cache


class SimpleCacheTestCase(TestCase):

    def test_get_set(self):
        c = cache.SimpleCache()
        c.set('foo', {'xyz': 'bar'})
        data = c.get('foo')
        self.assertEquals(data, {'xyz': 'bar'})

    def test_get_set_resource_id(self):
        c = cache.SimpleCache()
        c.set('foo', {'id': 100, 'xyz': 'bar'})
        data = c.get('foo', 100)
        self.assertEquals(data, {'id': 100, 'xyz': 'bar'})

    def test_get_many_resource_id(self):
        c = cache.SimpleCache()
        c.set('a', {'id': 1, 0: 0})
        c.set('a', {'id': 2, 1: 1})

        self.assertEquals(c.get_many('a', (1, 2)), [
            {'id': 1, 0: 0},
            {'id': 2, 1: 1},
        ])

    def test_set_many(self):
        c = cache.SimpleCache()
        c.set_many('foo', [
            {'id': 1, 0: 0},
            {'id': 2, 1: 1},
            {'id': 3, 2: 4},
        ])
        self.assertEquals(c.get('foo', 2), {'id': 2, 1: 1})
        c.set_many('foo', [{'id': 2, 1: 100}])
        self.assertEquals(c.get('foo', 2), {'id': 2, 1: 100})

    def test_delete(self):
        c = cache.SimpleCache()
        c.set('xyz', {'foo': 'bar'})
        self.assertEquals(c.get('xyz'), {'foo': 'bar'})
        c.delete('xyz')
        self.assertEquals(c.get('xyz'), None)


def _redis_installed():
    """Returns True if and only if the redis module is available"""
    try:
        import redis  # NOQA
        return True
    except ImportError:
        return False


@skipUnless(_redis_installed(), 'redis is not installed')
class RedisCacheTestCase(TestCase):
    def make_cache(self):
        return cache.RedisCache(key_prefix='gapi-python-client-test-case:')

    def tearDown(self):
        self.make_cache().clear()

    def test_get_set(self):
        c = self.make_cache()
        c.set('a', {'id': 1})
        self.assertEquals(c.get('a', 1), {'id': 1})

        c.set('a', {'results': (1, 2, 3)})
        self.assertEquals(c.get('a'), {'results': (1, 2, 3)})

    def test_get_many(self):
        c = self.make_cache()
        c.set('a', {'id': 1})
        c.set('a', {'id': 2})
        self.assertEquals(c.get_many('a', (1, 2)), [
            {'id': 1},
            {'id': 2},
        ])

    def test_set_many(self):
        c = self.make_cache()
        c.set_many('a', [
            {'id': 1, 0: 0},
            {'id': 2, 1: 1},
            {'id': 3, 2: 4},
        ])
        self.assertEquals(c.get('a', 3), {'id': 3, 2: 4})

    def test_expire(self):
        c = self.make_cache()
        c.set('expire_me', {0: 0}, timeout=1)
        time.sleep(2)
        self.assertEquals(c.get('expire_me'), None)

    def test_delete(self):
        c = self.make_cache()
        c.set('delete_me', {0: 0})
        self.assertEquals(c.get('delete_me'), {0: 0})
        c.delete('delete_me')
        self.assertEquals(c.get('delete_me'), None)
