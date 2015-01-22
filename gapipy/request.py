import requests

from . import __title__, __version__


ACCEPTABLE_RESPONSE_STATUS_CODES = (
    requests.codes.ok, requests.codes.created, requests.codes.accepted,
)

JSON_CONTENT_TYPE = 'application/json'

class APIRequestor(object):

    def __init__(self, client, resource, options=None, parent=None):
        self.client = client
        self.resource = resource
        self.options = options
        self.parent = parent

    def _request(self, uri, method, data=None, options=None, additional_headers=None):
        """Make an HTTP request to a target API method with proper headers."""

        assert method in ['GET', 'POST', 'PUT', 'PATCH'], "Only 'GET', 'POST', 'PUT', and 'PATCH' are allowed."

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

        headers = {
            'User-Agent': '{0}/{1}'.format(__title__, __version__),
            'X-Application-Key': self.client.application_key,
        }

        # gapipy works in JSON. Ensure the receiving API is aware of the type of
        # payload being sent.
        if method in ('POST', 'PUT', 'PATCH'):
            headers['Content-Type'] = JSON_CONTENT_TYPE

        if self.client.api_language:
            headers['Accept-Language'] = self.client.api_language

        if additional_headers:
            headers.update(additional_headers)

        if api_proxy:
            headers.update({'X-Api-Proxy': api_proxy})

        requests_call = getattr(requests, method.lower())

        self.client.logger.debug('Making a {0} request to {1}'.format(method, url))
        response = requests_call(url, headers=headers, data=data, params=options)

        if response.status_code in ACCEPTABLE_RESPONSE_STATUS_CODES:
            return response.json()
        else:
            response.reason = response.text
            return response.raise_for_status()

    def get(self, resource_id=None, uri=None):
        """Get a single resource with the given resource_id or uri"""

        if not (resource_id or uri):
            raise ValueError(
                'Need to provide at least one of `resource_id` or `uri` as argument')
        if not uri:
            uri = '/{0}/{1}'.format(self.resource, resource_id)
        return self._request(uri, 'GET')

    def update(self, resource_id, data, partial=True, uri=None):
        """
        Update a single resource with the given data.

        When `partial` is True, the http method is `PATCH`. Otherwise, `PUT` is
        sent.
        """
        method = 'PATCH' if partial else 'PUT'
        if not uri:
            uri = '/{0}/{1}'.format(self.resource, resource_id)
        return self._request(uri, method, data=data)

    def create(self, data, uri=None):
        """
        Create a single new resource with the given data.
        """
        if not uri:
            uri = '/{0}'.format(self.resource)
        return self._request(uri, 'POST', data=data)

    def list_raw(self, uri=None):
        """Return the raw response for listing resources.

        If `uri` is given, make a GET request to it, otherwise build the uri
        from `self.resource` and `self.parent`. Note that only the first page
        of results will be returned. To get an iterator over all resources,
        use `list`.
        """
        if not uri:
            if self.parent:
                parent_name, parent_id = self.parent
                uri = '/{0}/{1}/{2}'.format(parent_name, parent_id, self.resource)
            else:
                uri = '/{0}'.format(self.resource)

        return self._request(uri, 'GET', options=self.options)

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
