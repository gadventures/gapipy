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
        c.set('foo:100', {'id': 100, 'xyz': 'bar'})
        data = c.get('foo:100')
        self.assertEquals(data, {'id': 100, 'xyz': 'bar'})

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
        self.assertEquals(c.get('a'), {'id': 1})

        c.set('a', {'results': (1, 2, 3)})
        self.assertEquals(c.get('a'), {'results': (1, 2, 3)})

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
