from functools import wraps
from itertools import islice

from requests import HTTPError
from requests.status_codes import codes

from .request import APIRequestor


# The default set of HTTP Status codes that will result in Query.get
# returning a `None` value.
#
# Since 2.25.0 (See: https://github.com/gadventures/gapipy/pull/119)
#
# This is now passed as default parameter to `Query.get`. This has allowed
# a slight modification to the behaviour of Resource.fetch, which now passes
# in an explicit `None` value for `httperrors_mapped_to_none` kwarg.`Query.get`
# will now raise the requests.HTTTPError when an attempt to `fetch` stub fails,
# providing more expressive errors to be bubbled up.
HTTPERRORS_MAPPED_TO_NONE = (
    codes.FORBIDDEN,  # 403
    codes.NOT_FOUND,  # 404
    codes.GONE,       # 410
)


def _check_listable(func):

    @wraps(func)
    def inner(query, *args, **kwargs):
        if not (query.resource._is_listable or query.parent):
            raise ValueError(
                'The {0} resource is not listable and/or is only available as a subresource'.format(
                    query.resource.__name__))

        return func(query, *args, **kwargs)

    return inner


class Empty:
    pass


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

    def options(self):
        return self.resource.options(client=self._client)

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
        key = self.query_key(resource_id, variation_id) # noqa

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
            part = self._client.application_key.split('_')[0]
            if part == self._client.application_key or part.strip(' ') != 'test':
                return ':'.join(parts)
            parts.append(part)
        return ':'.join(parts)

    def _clone(self):
        """
        Object cloner
        """
        obj = Empty()
        obj.__class__ = self.__class__
        for attr, value in self.__dict__.items():
            setattr(obj, attr, value)
        return obj

    @_check_listable
    def all(self, limit=None):
        """Generator of instances of the query resource. If limit is set to a
        positive integer `n`, only return the first `n` results.
        """
        obj = self._clone()

        requestor = APIRequestor(
            obj._client,
            obj.resource,
            params=obj._filters,
            parent=obj.parent
        )
        # use href when available; this change should be transparent
        # introduced: 2.20.0
        href = None
        if isinstance(obj._raw_data, dict):
            href = obj._raw_data.get('href')

        # generator to fetch list resources
        generator = requestor.list(href)

        if limit:
            if isinstance(limit, int) and limit > 0:
                generator = islice(generator, limit)
            else:
                raise ValueError('`limit` must be a positive integer')

        for result in generator:
            yield obj.resource(result, client=obj._client, stub=True)

    def filter(self, **kwargs):
        """Add filter arguments to the query.

        For example, if `query` is a Query for the TourDossier ressource, then
        `query.filter(name='Amazing Adventure')` will return a query containing
        only dossiers whose names contain 'Amazing Adventure'.
        """
        self._filters.update(kwargs)
        obj = self._clone()

        # we have clear here else next filter call will inherit from the
        # stacked filters. Necessary if we want to preserve the instance independence
        self._filters = {}

        return obj

    @_check_listable
    def count(self):
        """Returns the number of element in the query."""

        obj = self._clone()

        requestor = APIRequestor(
            obj._client,
            obj.resource,
            params=obj._filters,
            parent=obj.parent
        )

        response = requestor.list_raw()
        out = response.get('count')

        return out

    def create(self, data_dict, headers=None):
        """Create an instance of the query resource using the given data"""
        return self.resource.create(self._client, data_dict, headers=headers)

    def first(self):
        """
        Returns the first object of a query, returns None if no match is found.
        """
        return next(self.all(), None)

    def __iter__(self):
        """Provided as a convenience so that Query objects can be iterated
        without calling `all`.

            i.e.  `for dossier in dossiers.filter(name='Peru')`
                instead of `for dossier in dossiers.filter(name='Peru').all()`
        """
        return self.all()
