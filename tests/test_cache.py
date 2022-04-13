import time
from unittest import TestCase, skip, skipUnless

from gapipy import cache

try:
    from unittest import mock  # Python 3
except ImportError:
    import mock  # Python 2

try:
    from django.test import override_settings
except ImportError:
    override_settings = lambda *__args, **__kwargs: skip


def _django_installed():
    """Returns True if and only if the django module is available"""
    try:
        import django  # NOQA
        return True
    except ImportError:
        return False


@skipUnless(_django_installed(), 'django is not installed')
class DjangoCacheTestCase(TestCase):
    def setUp(self):
        self.cache_patcher = mock.patch("gapipy.cache.django_caches")
        self.mock_cache = self.cache_patcher.start()['gapi']
        self.addCleanup(self.cache_patcher.stop)

        self.default_settings_override = override_settings(CACHES={'gapi': {}})
        self.default_settings_override.enable()
        self.addCleanup(self.default_settings_override.disable)

        self.client = cache.DjangoCache()

    @override_settings(CACHES=None)
    def test_caches_required(self):
        """Should require CACHES setting."""
        self.assertRaises(AssertionError, cache.DjangoCache)

    @override_settings(CACHES={})
    def test_gapi_cache_settings_required(self):
        """Should require 'gapi' CACHES settings."""
        self.assertRaises(AssertionError, cache.DjangoCache)

    def test_clear(self):
        """Should delegate 'clear' operation to django cache client."""
        self.client.clear()
        self.mock_cache.clear.assert_called_once()

    def test_delete(self):
        """Should delegate 'delete' operation to django cache client."""
        self.client.delete('test-key')
        self.mock_cache.delete.assert_called_once_with('test-key')

    def test_get(self):
        """Should delegate 'get' operation to django cache client."""
        self.client.get('test-key')
        self.mock_cache.get.assert_called_once_with('test-key')

    def test_is_cached(self):
        """Should delegate 'is_cached' to django cache client __contains__"""
        self.client.is_cached('test-key')
        self.mock_cache.__contains__.assert_called_once_with('test-key')

    def test_set(self):
        """Should delegate 'set' operation to django cache client."""
        self.client.set('test-key', 'test-value', 'test-timeout')
        self.mock_cache.set.assert_called_once_with('test-key', 'test-value', 'test-timeout')

    def test_set__default_timeout(self):
        """Should delegate 'set' operation to django cache client with default cache timeout."""
        self.client.set('test-key', 'test-value', timeout=None)
        self.mock_cache.set.assert_called_once_with('test-key', 'test-value', self.client.default_timeout)



class SimpleCacheTestCase(TestCase):

    def test_get_set(self):
        c = cache.SimpleCache()
        c.set('foo', {'xyz': 'bar'})
        data = c.get('foo')
        self.assertEqual(data, {'xyz': 'bar'})

    def test_get_set_resource_id(self):
        c = cache.SimpleCache()
        c.set('foo:100', {'id': 100, 'xyz': 'bar'})
        data = c.get('foo:100')
        self.assertEqual(data, {'id': 100, 'xyz': 'bar'})

    def test_delete(self):
        c = cache.SimpleCache()
        c.set('xyz', {'foo': 'bar'})
        self.assertEqual(c.get('xyz'), {'foo': 'bar'})
        c.delete('xyz')
        self.assertEqual(c.get('xyz'), None)


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
        self.assertEqual(c.get('a'), {'id': 1})

        c.set('a', {'results': (1, 2, 3)})
        self.assertEqual(c.get('a'), {'results': (1, 2, 3)})

    def test_expire(self):
        c = self.make_cache()
        c.set('expire_me', {0: 0}, timeout=1)
        time.sleep(2)
        self.assertEqual(c.get('expire_me'), None)

    def test_delete(self):
        c = self.make_cache()
        c.set('delete_me', {0: 0})
        self.assertEqual(c.get('delete_me'), {0: 0})
        c.delete('delete_me')
        self.assertEqual(c.get('delete_me'), None)
