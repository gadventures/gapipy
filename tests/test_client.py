import json
import unittest

from gapipy.client import Client
from gapipy.query import Query
from gapipy.resources.base import Resource
from gapipy.utils import get_available_resource_classes

try:
    from unittest import mock  # Python 3
except ImportError:
    import mock  # Python 2


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.gapi = Client()

    def test_resource_querysets_available(self):
        for resource in [r._resource_name for r in get_available_resource_classes()]:
            self.assertTrue(hasattr(self.gapi, resource))
            self.assertIsInstance(getattr(self.gapi, resource), Query)

    def test_query_interface(self):
        resource_name = get_available_resource_classes()[0]._resource_name
        self.assertTrue(isinstance(self.gapi.query(resource_name), Query))

    def test_unavailable_resource_query(self):
        with self.assertRaises(AttributeError):
            self.gapi.query("fake_resource")

    def test_build_interface(self):
        class MockResource(Resource):
            _as_is_fields = ['id', 'foo']
            _resource_name = 'foo'
        self.gapi.foo = Query(self.gapi, MockResource)

        resource = self.gapi.build('foo', {'id': 1, 'foo': 'bar'})

        self.assertEqual(resource.id, 1)
        self.assertEqual(resource.foo, 'bar')

    @mock.patch('gapipy.request.APIRequestor._request')
    def test_create_interface(self, mock_request):
        class MockResource(Resource):
            _as_is_fields = ['id', 'foo']
            _resource_name = 'foo'
        self.gapi.foo = Query(self.gapi, MockResource)

        # On create, a representation of the resource is created.
        mock_request.return_value = {
            'id': 1,
            'foo': 'bar',
        }

        # Create allows arbitrary data to be sent, even if it's not part of the
        # final resource.
        resource = self.gapi.create('foo', {'id': 1, 'foo': 'bar', 'context': 'abc'})
        self.assertEqual(resource.id, 1)

    @mock.patch('gapipy.request.APIRequestor._request')
    def test_create_extra_headers(self, mock_request):
        """
        Test that extra HTTP headers can be passed through the `.create`
        method on a resource
        """
        class MockResource(Resource):
            _as_is_fields = ['id', 'foo']
            _resource_name = 'foo'
        self.gapi.foo = Query(self.gapi, MockResource)

        resource_data = {'id': 1, 'foo': 'bar'}  # content doesn't really matter for this test
        mock_request.return_value = resource_data

        # Create a `foo` while passing extra headers
        extra_headers = {'X-Bender': 'I\'m not allowed to sing. Court order.'}
        self.gapi.create('foo', resource_data, headers=extra_headers)

        # Did those headers make it all the way to the requestor?
        mock_request.assert_called_once_with(
            '/foo',
            'POST',
            data=json.dumps(resource_data),
            additional_headers=extra_headers,
        )

    @mock.patch('gapipy.query.Query.get_resource_data')
    def test_correct_client_is_associated_with_resources(self, mock_get_data):
        mock_get_data.return_value = {
            'id': 123
        }
        en_client = Client(api_language='en')
        de_client = Client(api_language='de')

        en_itin = en_client.itineraries.get(123)
        de_itin = de_client.itineraries.get(123)

        self.assertEqual(en_itin._client, en_client)
        self.assertEqual(de_itin._client, de_client)

    def test_default_retries(self):
        """Should not set any retries on the client's requestor."""
        http_retries = self.gapi.requestor.adapters['http://'].max_retries.total
        https_retries = self.gapi.requestor.adapters['https://'].max_retries.total

        self.assertEqual(http_retries, 0)
        self.assertEqual(https_retries, 0)

    def test_retries_no_connection_pooling(self):
        """Should initialize the client's requestor with the passed number of retries."""
        expected_retries = 42
        client_with_retries = Client(max_retries=expected_retries)

        # Connection pooling defaults to https only
        https_retries = client_with_retries.requestor.adapters['https://'].max_retries.total

        self.assertEqual(https_retries, expected_retries)

    def test_retries_with_connection_pooling(self):
        """Should initialize the client's requestor with the passed number of retries."""
        expected_retries = 84
        connection_pool_options = {"enable": True}

        client_with_retries = Client(max_retries=expected_retries, connection_pool_options=connection_pool_options)

        # Connection pooling defaults to https only
        https_retries = client_with_retries.requestor.adapters['https://'].max_retries.total

        self.assertEqual(https_retries, expected_retries)

