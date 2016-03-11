from functools import wraps
from itertools import islice

from requests import HTTPError

from .request import APIRequestor


def _check_listable(func):

    @wraps(func)
    def inner(query, *args, **kwargs):
        if not (query.resource._is_listable or query.parent):
            raise ValueError(
                'The {0} resource is not listable and/or is only available as a subresource'.format(
                    query.resource.__name__))

        return func(query, *args, **kwargs)

    return inner


class Query(object):

    def __init__(self, client, resource, filters=None, parent=None, raw_data=None):
        self._client = client
        self._raw_data = raw_data or {}
        self.resource = resource
        self._filters = filters or {}
        self.parent = parent

    def _to_dict(self):
        # Used by Resource when converting nested Query objects into
        # serializable types.
        return self._raw_data

    def get(self, resource_id, variation_id=None, cached=True):
        """
        Returns an instance of the query resource with the given `resource_id`
        (and optional `variation_id`) or `None` if the resource with the given
        id does not exist.

        If the resource is available in the cache and `cached` is True, no http
        request will be made. If `cached` is False, a fresh request will be
        made for the resource, which will be re-added to the cache. This is a
        good method to invalidate persistent cache backend after receiving a
        webhook that a resource has changed.
        """
        key = self.query_key(resource_id, variation_id)

        try:
            data = self.get_resource_data(
                resource_id,
                variation_id=variation_id,
                cached=cached
            )
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise e
        resource_object = self.resource(data, client=self._client)
        self._client._cache.set(key, resource_object.to_dict())
        return resource_object

    def get_resource_data(self, resource_id, variation_id=None, cached=True):
        '''
        Returns a dictionary of resource data, which is used to initialize
        a Resource object in the `get` method.
        '''
        key = self.query_key(resource_id, variation_id)
        resource_data = None
        if cached:
            resource_data = self._client._cache.get(key)
            if resource_data is not None:
                return resource_data

        # Cache miss; get fresh data from the backend.
        requestor = APIRequestor(self._client, self.resource._resource_name)
        out = requestor.get(resource_id, variation_id=variation_id)
        self._filters = {}
        return out

    def purge_cached(self, resource_id, variation_id=None):
        key = self.query_key(resource_id, variation_id)
        return self._client._cache.delete(key)

    def is_cached(self, resource_id, variation_id=None):
        key = self.query_key(resource_id, variation_id)
        return self._client._cache.is_cached(key)

    def query_key(self, resource_id=None, variation_id=None):
        """Returns a unique key for the information used to fetch the resource(s)
        in this query. Currently used for creating cache keys.
        """
        if not resource_id:
            return self.resource._resource_name

        parts = [self.resource._resource_name, str(resource_id)]
        if variation_id:
            parts.append(str(variation_id))
        if self._client.api_language:
            parts.append(self._client.api_language)

        if self._client.application_key:
            part = self._client.application_key.split('_')[0]
            if part == self._client.application_key or part.strip(' ') != 'test':
                return ':'.join(parts)
            parts.append(part)
        return ':'.join(parts)

    @_check_listable
    def all(self, limit=None):
        """Generator of instances of the query resource. If limit is set to a
        positive integer `n`, only return the first `n` results.
        """

        requestor = APIRequestor(
            self._client,
            self.resource._resource_name,
            params=self._filters,
            parent=self.parent
        )
        generator = requestor.list()

        if limit:
            if isinstance(limit, int) and limit > 0:
                generator = islice(generator, limit)
            else:
                raise ValueError('`limit` must be a positive integer')

        for result in generator:
            yield self.resource(result, client=self._client, stub=True)

    def filter(self, **kwargs):
        """Add filter arguments to the query.

        For example, if `query` is a Query for the TourDossier ressource, then
        `query.filter(name='Amazing Adventure')` will return a query containing
        only dossiers whose names contain 'Amazing Adventure'.
        """
        self._filters.update(kwargs)
        return self

    @_check_listable
    def count(self):
        """Returns the number of element in the query."""

        requestor = APIRequestor(
            self._client,
            self.resource._resource_name,
            params=self._filters,
            parent=self.parent
        )
        response = requestor.list_raw()
        out = response.get('count')
        self._filters = {}
        return out

    def create(self, data_dict):
        """Create an instance of the query resource using the given data"""
        return self.resource.create(self._client, data_dict)

    def __iter__(self):
        """Provided as a convenience so that Query objects can be iterated
        without calling `all`.

            i.e.  `for dossier in dossiers.filter(name='Peru')`
                instead of `for dossier in dossiers.filter(name='Peru').all()`
        """
        return self.all()
