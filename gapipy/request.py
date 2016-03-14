import requests

from . import __title__, __version__


ACCEPTABLE_RESPONSE_STATUS_CODES = (
    requests.codes.ok, requests.codes.created, requests.codes.accepted,
)

JSON_CONTENT_TYPE = 'application/json'


class APIRequestor(object):

    def __init__(self, client, resource, params=None, parent=None):
        self.client = client
        self.resource = resource
        self.params = params
        self.parent = parent

    def _request(self, uri, method, data=None, params=None, additional_headers=None):
        """Make an HTTP request to a target API method with proper headers."""

        assert method in ['GET', 'POST', 'PUT', 'PATCH'], "Only 'GET', 'POST', 'PUT', and 'PATCH' are allowed."
        url = self._get_url(uri)
        headers = self._get_headers(method, additional_headers)
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

    def get(self, resource_id=None, uri=None, variation_id=None):
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
            components = ['', self.resource, str(resource_id)]
            if variation_id:
                components.append(str(variation_id))
            uri = '/'.join(components)
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
                parent_name, parent_id, parent_variation_id = self.parent

                # First slash ensures leading slash.
                parts = [parent_name, parent_id]
                if parent_variation_id:
                    parts.append(parent_variation_id)

                parts.append(self.resource)

                # Ensure leading slash.
                uri = '/' + '/'.join(parts)
            else:
                uri = '/{0}'.format(self.resource)

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
