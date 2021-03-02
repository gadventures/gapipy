from copy import deepcopy
from functools import wraps
from itertools import islice

from requests import HTTPError

from .constants import HTTPERRORS_MAPPED_TO_NONE
from .request import APIRequestor


def _check_listable(func):
    """
    decorator to ensure the Query we're attempting to call func on is listable
    """
    @wraps(func)
    def wrapper(query, *args, **kwargs):
        if not (query.resource._is_listable or query.parent):
            raise ValueError(
                "The {} resource is not listable and/or is only available as a subresource".format(
                    query.resource.__name__,
                )
            )
        return func(query, *args, **kwargs)

    return wrapper


class Query(object):

    def __init__(self, client, resource, filters=None, parent=None, raw_data=None):
        self.parent = parent
        self.resource = resource
        self._client = client
        self._filters = filters or {}
        self._raw_data = raw_data or {}

    def __iter__(self):
        """Provided as a convenience so that Query objects can be iterated
        without calling `all`.

        i.e.  `for dossier in dossiers.filter(name="Peru")`
              instead of `for dossier in dossiers.filter(name="Peru").all()`
        """
        return self.all()

    def _to_dict(self):
        # Used by Resource when converting nested Query objects into
        # serializable types.
        return self._raw_data

    def _clone(self):
        """
        create a clone of this Query, with deep copies of _filter & _raw_data
        """
        return Query(
            self._client,
            self.resource,
            filters=deepcopy(self._filters),
            parent=self.parent,
            raw_data=deepcopy(self._raw_data),
        )

    def get(self, resource_id, variation_id=None, cached=True, headers=None,
            httperrors_mapped_to_none=HTTPERRORS_MAPPED_TO_NONE):
        """
        Returns an instance of the query resource with the given `resource_id`
        (and optional `variation_id`).

        If the resource is available in the cache and `cached` is True, no http
        request will be made. If `cached` is False, a fresh request will be
        made for the resource, which will be re-added to the cache. This is a
        good method to invalidate persistent cache backend after receiving a
        webhook that a resource has changed.

        If an HTTP error code within `httperrors_mapped_to_none` is raised,
        this method will return `None` -- see `HTTPERRORS_MAPPED_TO_NONE` for
        the default list of errors which cause a `None` return. If you wish to
        allow all raised `HTTPErrors` to escape this method, you can pass
        something Falsey as `httperrors_mapped_to_none` like a `None` or an
        empty list.
        """
        try:
            data = self.get_resource_data(
                resource_id,
                variation_id=variation_id,
                cached=cached,
                headers=headers
            )
        except HTTPError as e:
            if httperrors_mapped_to_none and e.response.status_code in httperrors_mapped_to_none:
                return None
            raise e
        resource_object = self.resource(data, client=self._client)
        return resource_object

    def get_resource_data(self, resource_id, variation_id=None, cached=True, headers=None):
        """
        Returns a dictionary of resource data, which is used to initialize
        a Resource object in the `get` method.
        """
        key = self.query_key(resource_id, variation_id)
        resource_data = None
        if cached:
            resource_data = self._client._cache.get(key)
            if resource_data is not None:
                return resource_data

        # Cache miss; get fresh data from the backend, set in cache
        requestor = APIRequestor(self._client, self.resource)
        out = requestor.get(resource_id, variation_id=variation_id, headers=headers)
        if out is not None:
            self._client._cache.set(key, out)
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
            part = self._client.application_key.split("_")[0]
            if part == self._client.application_key or part.strip(" ") != "test":
                return ":".join(parts)
            parts.append(part)
        return ":".join(parts)

    @_check_listable
    def all(self, limit=None):
        """Generator of instances of the query resource. If limit is set to a
        positive integer `n`, only return the first `n` results.
        """
        # check limit is valid integer value
        if limit is not None:
            if not isinstance(limit, int):
                raise TypeError("limit must be an integer")
            elif limit <= 0:
                raise ValueError("limit must be a positive integer")

        requestor = APIRequestor(
            self._client,
            self.resource,
            params=self._filters,
            parent=self.parent
        )
        # use href when available; this change should be transparent
        # introduced: 2.20.0
        href = None
        if isinstance(self._raw_data, dict):
            href = self._raw_data.get("href")

        # generator to fetch list resources
        for result in islice(requestor.list(href), limit):
            yield self.resource(result, client=self._client, stub=True)

    def filter(self, **kwargs):
        """Add filter arguments to the query.

        For example, if `query` is a Query for the TourDossier ressource, then
        `query.filter(name="Amazing Adventure")` will return a query containing
        only dossiers whose names contain "Amazing Adventure".
        """
        clone = self._clone()
        clone._filters.update(kwargs)
        return clone

    @_check_listable
    def count(self):
        """Returns the number of element in the query."""
        requestor = APIRequestor(
            self._client,
            self.resource,
            params=self._filters,
            parent=self.parent
        )
        return requestor.list_raw().get("count")

    def create(self, data_dict, headers=None):
        """Create an instance of the query resource using the given data"""
        return self.resource.create(self._client, data_dict, headers=headers)

    def first(self):
        """
        Returns the first object of a query, returns None if no match is found.
        """
        return next(self.all(), None)

    def options(self):
        """
        return the OPTIONS response for the resource bound to this Query
        """
        return self.resource.options(client=self._client)
