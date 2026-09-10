import logging
import os
import re
from importlib import import_module

from .utils import get_available_resource_classes

# initialise logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


# the default configuration dict with values pulled from the environment
default_config = {
    'api_language': os.environ.get('GAPI_LANGUAGE'),
    'api_proxy': os.environ.get('GAPI_API_PROXY', ''),
    'api_root': os.environ.get('GAPI_API_ROOT', 'https://rest.gadventures.com'),
    'application_key': os.environ.get('GAPI_APPLICATION_KEY'),
    'cache_backend': os.environ.get('GAPI_CACHE_BACKEND', 'gapipy.cache.NullCache'),
    'async_cache_backend': os.environ.get('GAPI_ASYNC_CACHE_BACKEND', 'gapipy.async_cache.AsyncNullCache'),
    'cache_options': {'threshold': 500, 'default_timeout': 3600},
    'connection_pool_options': {
        'enable': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_ENABLE', False),
        'block': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_BLOCK', False),
        'number': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_NUMBER', 10),
        'maxsize': os.environ.get('GAPI_CLIENT_CONNECTION_POOL_MAXSIZE', 10),
    },
    'debug': os.environ.get('GAPI_CLIENT_DEBUG', False),
    'max_retries': os.environ.get('GAPI_CLIENT_MAX_RETRIES', 0),
    'raise_on_empty_update': os.environ.get('GAPI_CLIENT_RAISE_ON_EMPTY_UPDATE', False),
    'uuid': os.environ.get('GAPI_UUID', False),
    # we don't have a nice way to intialise a dictionary from the environment,
    # so we default it to an empty dict here.
    'global_http_headers': {},
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


class _BaseClient(object):
    """Shared extension seams and common config for sync + async Clients."""

    @classmethod
    def register_config_defaults(cls, defaults):
        """Merge keys into default_config; applies to future Clients only."""
        default_config.update(defaults)

    def _init_seams(self):
        """Initialize the registry + callback lists. Call from subclass __init__."""
        self._resource_registry = {}
        self._response_callbacks = []

    def _load_common_config(self, config):
        """Read the config keys sync and async Clients share."""
        self.api_language = get_config(config, 'api_language')
        self.api_proxy = get_config(config, 'api_proxy')
        self.api_root = get_config(config, 'api_root')
        self.application_key = get_config(config, 'application_key')
        self.global_http_headers = get_config(config, 'global_http_headers')
        self.max_retries = get_config(config, 'max_retries')
        self.raise_on_empty_update = get_config(config, 'raise_on_empty_update')
        self.uuid = get_config(config, 'uuid')

    def register_resource(self, resource_cls):
        """Register a resource class, keyed by both class name and _resource_name."""
        self._resource_registry[resource_cls.__name__] = resource_cls
        self._resource_registry[resource_cls._resource_name] = resource_cls

    def get_resource_class_by_name(self, name):
        """Resolve a resource class by class name or _resource_name."""
        return self._resource_registry[name]

    def on_response(self, callback):
        """Register a post-response callback fired with the raw Response."""
        self._response_callbacks.append(callback)

    def _attach_queries(self, query_cls):
        """Register built-in resources and hang a `query_cls` per resource off `self`."""
        for resource in get_available_resource_classes():
            self.register_resource(resource)
            setattr(self, resource._resource_name, query_cls(self, resource))


class Client(_BaseClient):

    def __init__(self, **config):
        self._load_common_config(config)
        self.cache_backend = get_config(config, 'cache_backend')

        # begin with default connection pool options and override them with
        # the configuration options the client has specified
        self.connection_pool_options = default_config['connection_pool_options']
        self.connection_pool_options.update(get_config(config, 'connection_pool_options'))

        log_level = 'DEBUG' if get_config(config, 'debug') else 'ERROR'
        self.logger = logger
        self.logger.setLevel(log_level)

        self._set_cache_instance(get_config(config, 'cache_options'))
        self._set_requestor(self.connection_pool_options, self.max_retries)

        self._init_seams()

        # Import Query lazily — top-level import breaks some CI environments
        # where `requests` isn't yet installed during setup.py discovery.
        from .query import Query
        self._attach_queries(Query)

    def _set_cache_instance(self, cache_options):
        cache_backend = self.cache_backend
        module_name, class_name = cache_backend.rsplit('.', 1)
        module = import_module(module_name)
        cache = getattr(module, class_name)(**cache_options)
        self._cache = cache

    def _set_requestor(self, pool_options, max_retries):
        """
        Set the requestor based on connection pooling options.

        If connection pooling is disabled, just set `requests`. If connection
        pooling is enabled, set up a `requests.Session`.
        """
        # We had been importing this at the top of the module, but that seemed
        # to break some CI environments
        import requests

        session = requests.Session()

        if not pool_options['enable']:
            adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        else:
            adapter = requests.adapters.HTTPAdapter(
                pool_block=pool_options['block'],
                pool_connections=pool_options['number'],
                pool_maxsize=pool_options['maxsize'],
                max_retries=max_retries,
            )
            logger.info(
                'Created connection pool (block=%s, number=%d, maxsize=%d)',
                pool_options['block'],
                pool_options['number'],
                pool_options['maxsize'],
            )

        prefix = _get_protocol_prefix(self.api_root)
        if prefix:
            session.mount(prefix, adapter)
            logger.info('Mounted session for "%s"', prefix)
        else:
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            logger.info(
                'Could not find protocol prefix in API root, mounted session '
                'on both http and https.'
            )

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

    def create(self, resource_name, data_dict, headers=None):
        """
        Create an instance of the specified resource with `data_dict`
        """
        try:
            resource_cls = getattr(self, resource_name).resource
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

        return resource_cls.create(self, data_dict, headers=headers)
