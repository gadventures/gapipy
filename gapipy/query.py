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
        self.filters = filters or {}
        self.parent = parent

    def _to_dict(self):
        # Used by Resource when converting nested Query objects into
        # serializable types.
        return self._raw_data

    def get(self, resource_id, cached=True):
        """
        Returns an instance of the query resource with the given `resource_id`,
        or `None` if the resource with the given id does not exist.

        If the resource is available in the cache and `cached` is True, no http
        request will be made. If `cached` is False, a fresh request will be
        made for the resource, which will be re-added to the cache. This is a
        good method to invalidate persistent cache backend after receiving a
        webhook that a resource has changed.
        """
        if cached:
            resource_data = self._client._cache.get(
                self.resource._resource_name,
                resource_id,
            )
            if resource_data is not None:
                return self.resource(resource_data)

        requestor = APIRequestor(self._client, self.resource._resource_name)

        try:
            data = requestor.get(resource_id)
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise e

        resource_object = self.resource(data)
        self._client._cache.set(self.resource._resource_name, resource_object.to_dict())
        return resource_object

    def purge_cached(self, resource_id):
        return self._client._cache.delete(
            self.resource._resource_name,
            resource_id,
        )

    def is_cached(self, resource_id):
        return self._client._cache.is_cached(
            self.resource._resource_name,
            resource_id
        )

    @_check_listable
    def all(self, limit=None):
        """Generator of instances of the query resource. If limit is set to a
        positive integer `n`, only return the first `n` results.
        """

        requestor = APIRequestor(
            self._client,
            self.resource._resource_name,
            options=self.filters,
            parent=self.parent
        )
        generator = requestor.list()

        if limit:
            if isinstance(limit, int) and limit > 0:
                generator = islice(generator, limit)
            else:
                raise ValueError('`limit` must be a positive integer')

        for result in generator:
            yield self.resource(result, stub=True)

    def filter(self, **kwargs):
        """Add filter arguments to the query.

        For example, if `query` is a Query for the TourDossier ressource, then
        `query.filter(name='Amazing Adventure')` will return a query containing
        only dossiers whose names contain 'Amazing Adventure'.
        """

        self.filters.update(kwargs)
        return self

    @_check_listable
    def count(self):
        """Returns the number of element in the query."""

        requestor = APIRequestor(
            self._client,
            self.resource._resource_name,
            options=self.filters,
            parent=self.parent
        )
        response = requestor.list_raw()
        return response.get('count')

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
