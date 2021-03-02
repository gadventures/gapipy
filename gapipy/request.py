import sys
from uuid import uuid1

from future.moves.urllib.parse import urlparse

from gapipy.constants import ACCEPTABLE_RESPONSE_STATUS_CODES
from gapipy.constants import ALLOWED_METHODS
from gapipy.constants import JSON_CONTENT_TYPE

from . import __title__, __version__


class APIRequestor(object):

    def __init__(self, client, resource, params=None, parent=None):
        self.client = client
        self.resource = resource
        self.params = params
        self.parent = parent

    def _request(self, uri, method, data=None, params=None, additional_headers=None):
        """Make an HTTP request to a target API method with proper headers."""

        assert method in ALLOWED_METHODS, "Only {} are allowed.".format(', '.join(ALLOWED_METHODS))
        url = self._get_url(uri)
        headers = self._get_headers(method, additional_headers)
        if self.client.uuid:
            if not params:
                params = {}
            params['uuid'] = str(uuid1())
        response = self._make_call(method, url, headers, data, params)
        return response

    def _get_url(self, uri):
        """Return the full URL to make a request to for the given `uri`"""

        # Support supplying a full url
        if '://' in uri:
            url = uri
        else:
            url = self.client.api_root + uri

        # Strip out the proxy from the url. The client only wants to return urls
        # with the API_PROXY, but not actually query on them.
        api_proxy = self.client.api_proxy
        if api_proxy:
            url = url.replace(api_proxy, '')

        return url

    def _get_headers(self, method, additional_headers):
        """Return a dictionary of HTTP headers to set on the request to the API."""

        # Start with an empty collection of headers
        headers = {}

        # If our client was configured to send some headers globally on all
        # requests, include those
        if self.client.global_http_headers:
            headers.update(self.client.global_http_headers)

        # Add the identification + auth headers
        headers.update({
            'User-Agent': '{0}/{1}'.format(__title__, __version__),
            'X-Application-Key': self.client.application_key,
        })

        # gapipy works in JSON. Ensure the receiving API is aware of the type of
        # payload being sent.
        if method in ('POST', 'PUT', 'PATCH'):
            headers['Content-Type'] = JSON_CONTENT_TYPE

        if self.client.api_language:
            headers['Accept-Language'] = self.client.api_language

        # If this specific call included additional headers, include them
        if additional_headers:
            headers.update(additional_headers)

        if self.client.api_proxy:
            headers.update({'X-Api-Proxy': self.client.api_proxy})

        return headers

    def _make_call(self, method, url, headers, data, params):
        """Make the actual request to the API, using the given URL, headers,
        data and extra parameters.
        """
        requests_call = getattr(self.client.requestor, method.lower())

        self.client.logger.debug('Making a {0} request to {1}'.format(method, url))

        response = requests_call(url, headers=headers, data=data, params=params)
        if response.status_code in ACCEPTABLE_RESPONSE_STATUS_CODES:
            return response.json()
        else:
            response.reason = response.text
            return response.raise_for_status()

    def _get_uri(self):
        # Python 2 has str, Python 3 basestring
            # Python 2
        if sys.version_info.major < 3:
            if isinstance(self.resource, basestring):
                return self.resource
        else:
            # Python 3
            if isinstance(self.resource, str):
                return self.resource

        if self.resource._uri:
            return self.resource._uri
        return self.resource._resource_name

    def options(self):
        """
        Get the options for a resource
        """
        return self._request('/{0}'.format(self._get_uri()), 'OPTIONS')

    def get(self, resource_id=None, uri=None, variation_id=None, headers=None):
        """
        Get a single resource with the given resource_id or uri

        If a resource_id is supplied, a variation_id may also be given -- when
        generating the URI, the variation_id will come after the resource_id,
        separated by a slash.
        """
        if resource_id is None and uri is None:
            raise ValueError(
                'Need to provide at least one of `resource_id` or `uri` as argument')
        if not uri:
            components = ['', self._get_uri(), str(resource_id)]
        if variation_id:
            components.append(str(variation_id))
        uri = '/'.join(components)
        return self._request(uri, 'GET', additional_headers=headers)

    def update(self, resource_id, data, partial=True, uri=None):
        """
        Update a single resource with the given data.

        When `partial` is True, the http method is `PATCH`. Otherwise, `PUT` is
        sent.
        """
        method = 'PATCH' if partial else 'PUT'
        if not uri:
            uri = '/{0}/{1}'.format(self._get_uri(), resource_id)
        return self._request(uri, method, data=data)

    def create(self, data, uri=None, headers=None):
        """
        Create a single new resource with the given data.
        """
        if not uri:
            uri = '/{0}'.format(self._get_uri())
        return self._request(uri, 'POST', data=data, additional_headers=headers)

    def list_raw(self, uri=None):
        """Return the raw response for listing resources.

        If `uri` is given, make a GET request to it; otherwise build the uri
        from `self.resource._uri`(if present) and `self.parent`; else
        `self.resource._resource_name` and `self.parent`. Note that only the
        first page of results will be returned. To get an iterator over all
        resources, use `list`.
        """
        # A uri is provided, the primary use case is that `list` has been
        # called and as GAPI's next hrefs preserve the parameter filters, we
        # don't want to duplicate them.
        if uri:
            # check if we have query parameters
            if urlparse(uri).query:
                return self._request(uri, 'GET')
            # otherwise use the params this requestor was initialised with
            return self._request(uri, 'GET', params=self.params)

        # No uri provided, build it and request it
        #
        # if this requestor has a parent, it implies we're fetching nested-list
        # of the resource. We need to build the uri prefix in the form
        # /parent/{id}[/{variation_id}]/{self._get_uri()}
        #
        # parent is a 3-Tuple. See: BaseModel._set_resource_collection_field
        if self.parent:
            parts = [
                self.parent.uri,
                self.parent.id,
                self.parent.variation_id,
                self._get_uri(),
            ]
            uri = '/{0}'.format('/'.join(filter(None, parts)))
        else:
            uri = '/{0}'.format(self._get_uri())

        return self._request(uri, 'GET', params=self.params)

    def list(self, uri=None):
        """Generator for listing resources"""

        response = self.list_raw(uri)
        for result in response['results']:
            yield result

        for link in response.get('links', []):
            if link['rel'] != 'next':
                continue
            for result in self.list(link['href']):
                yield result
