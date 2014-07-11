import logging
import os
from importlib import import_module

from .utils import get_available_resource_classes


current_client = None

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

default_config = {
    'application_key': os.environ.get('GAPI_APPLICATION_KEY'),
    'api_root': os.environ.get('GAPI_API_ROOT', 'https://rest.gadventures.com'),
    'api_proxy': os.environ.get('GAPI_API_PROXY', ''),
    'api_language': os.environ.get('GAPI_LANGUAGE', 'en'),
    'cache_backend': os.environ.get('GAPI_CACHE_BACKEND', 'gapipy.cache.SimpleCache'),
    'cache_options': {'threshold': 500, 'default_timeout': 3600},
    'debug': os.environ.get('GAPI_CLIENT_DEBUG', False),
}


def get_config(config, name):
    return config.get(name, default_config[name])


class Client(object):

    def __init__(self, **config):

        global current_client
        current_client = self

        self.application_key = get_config(config, 'application_key')
        self.api_root = get_config(config, 'api_root')
        self.api_proxy = get_config(config, 'api_proxy')
        self.api_language = get_config(config, 'api_language')
        self.cache_backend = get_config(config, 'cache_backend')

        log_level = 'DEBUG' if get_config(config, 'debug') else 'ERROR'
        self.logger = logger
        self.logger.setLevel(log_level)

        self._set_cache_instance(get_config(config, 'cache_options'))

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

    def query(self, resource_name):
        try:
            return getattr(self, resource_name)
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

    def build(self, resource_name, data_dict, **kwargs):
        try:
            resource_cls = getattr(self, resource_name).resource
            return resource_cls(data_dict, **kwargs)
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

    def create(self, resource_name, data_dict):
        """
        Create an instance of the specified resource with `data_dict`
        """
        try:
            resource_cls = getattr(self, resource_name).resource
        except AttributeError:
            raise AttributeError("No resource named %s is defined." % resource_name)

        return resource_cls.create(self, data_dict)
