import logging
import os
import re
from importlib import import_module

from .utils import get_available_resource_classes


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

default_config = {
    'application_key': os.environ.get('GAPI_APPLICATION_KEY'),
    'api_root': os.environ.get('GAPI_API_ROOT', 'https://rest.gadventures.com'),
    'api_proxy': os.environ.get('GAPI_API_PROXY', ''),
    'api_language': os.environ.get('GAPI_LANGUAGE'),
    'cache_backend': os.environ.get('GAPI_CACHE_BACKEND', 'gapipy.cache.NullCache'),
    'cache_options': {'threshold': 500, 'default_timeout': 3600},
    'debug': os.environ.get('GAPI_CLIENT_DEBUG', False),
    'connection_pool_options': {
        'enable': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_ENABLE', False),
        'block': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_BLOCK', False),
        'number': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_NUMBER', 10),
        'maxsize': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_MAXSIZE', 10),
    },
}


def _get_protocol_prefix(api_root):
    """
    Returns the protocol plus "://" of api_root.

    This is likely going to be "https://".
    """
    match = re.search(r'^[^:/]*://', api_root)
    return match.group(0) if match else ''


def get_config(config, name):
    return config.get(name, default_config[name])


class Client(object):

    def __init__(self, **config):
        self.application_key = get_config(config, 'application_key')
        self.api_root = get_config(config, 'api_root')
        self.api_proxy = get_config(config, 'api_proxy')
        self.api_language = get_config(config, 'api_language')
        self.cache_backend = get_config(config, 'cache_backend')

        # begin with default connection pool options and overwrite any that the
        # client has specified
        self.connection_pool_options = default_config['connection_pool_options']
        self.connection_pool_options.update(get_config(config, 'connection_pool_options'))

        log_level = 'DEBUG' if get_config(config, 'debug') else 'ERROR'
        self.logger = logger
        self.logger.setLevel(log_level)

        self._set_cache_instance(get_config(config, 'cache_options'))
        self._set_requestor(self.connection_pool_options)

        # Prevent install issues where setup.py digs down the path and
        # eventually fails on a missing requests requirement by importing Query
        # only where it's needed.
        from .query import Query
        for resource in get_available_resource_classes():
            setattr(self, resource._resource_name, Query(self, resource))

    def _set_cache_instance(self, cache_options):
        cache_backend = self.cache_backend
        module_name, class_name = cache_backend.rsplit('.', 1)
        module = import_module(module_name)
        cache = getattr(module, class_name)(**cache_options)
        self._cache = cache

    def _set_requestor(self, pool_options):
        """
        Set the requestor based on connection pooling options.

        If connection pooling is disabled, just set `requests`. If connection
        pooling is enabled, set up a `requests.Session`.
        """
        # We had been importing this at the top of the module, but that seemed
        # to break some CI environments
        import requests

        if not pool_options['enable']:
            self._requestor = requests
            return

        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_block=pool_options['block'],
            pool_connections=pool_options['number'],
            pool_maxsize=pool_options['maxsize'],
        )
        logger.info(
            'Created connection pool (block={}, number={}, maxsize={})'.format(
                pool_options['block'],
                pool_options['number'],
                pool_options['maxsize']))

        prefix = _get_protocol_prefix(self.api_root)
        if prefix:
            session.mount(prefix, adapter)
            logger.info('Mounted connection pool for "{}"'.format(prefix))
        else:
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            logger.info(
                'Could not find protocol prefix in API root, mounted '
                'connection pool on both http and https.')

        self._requestor = session

    @property
    def requestor(self):
        """
        Return a requestor, an object we'll use to make HTTP requests.

        This is either going to be `requests` (if connection pooling is
        disabled), or a `requests.Session` (if connection pooling is enabled), or
        an AttributeError (if `__init__` has not happened yet).
        """
        return self._requestor

    def query(self, resource_name):
        try:
            return getattr(self, resource_name)
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

    def build(self, resource_name, data_dict, **kwargs):
        try:
            resource_cls = getattr(self, resource_name).resource
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

        return resource_cls(data_dict, client=self, **kwargs)

    def create(self, resource_name, data_dict):
        """
        Create an instance of the specified resource with `data_dict`
        """
        try:
            resource_cls = getattr(self, resource_name).resource
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

        return resource_cls.create(self, data_dict)
