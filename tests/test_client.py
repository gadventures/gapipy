from mock import patch
import unittest

from gapipy.client import Client
from gapipy.query import Query
from gapipy.resources.base import Resource
from gapipy.utils import get_available_resource_classes


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

        self.assertEquals(resource.id, 1)
        self.assertEquals(resource.foo, 'bar')

    @patch('gapipy.request.APIRequestor._request')
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
        self.assertEquals(resource.id, 1)

    @patch('gapipy.query.Query.get_resource_data')
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
