import unittest

from mock import call, patch

from gapipy.client import Client
from gapipy.request import APIRequestor

from .fixtures import FIRST_PAGE_LIST_DATA, SECOND_PAGE_LIST_DATA


@patch('gapipy.request.APIRequestor._request')
class APIRequestorTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_resource_by_id(self, mock_request):
        requestor = APIRequestor(self.client, 'resources')
        requestor.get(1234)
        mock_request.assert_called_once_with('/resources/1234', 'GET')

    def test_get_with_null_resource_id_and_uri_raises_error(self, mock_request):
        requestor = APIRequestor(self.client, 'resources')
        error_msg = 'Need to provide at least one of `resource_id` or `uri` as argument'
        with self.assertRaisesRegexp(ValueError, error_msg):
            requestor.get()

    def test_get_with_falsy_resource_id_does_not_raise_error(self, mock_request):
        requestor = APIRequestor(self.client, 'resources')
        requestor.get(0)
        mock_request.assert_called_once_with('/resources/0', 'GET')

    def test_list_resource(self, mock_request):
        requestor = APIRequestor(self.client, 'resources')
        requestor.list_raw()
        mock_request.assert_called_once_with('/resources', 'GET', params=None)

    def test_list_resource_with_parent(self, mock_request):
        parent = ('parent', '1234', None)
        requestor = APIRequestor(self.client, 'child', parent=parent)
        requestor.list_raw()
        mock_request.assert_called_once_with(
            '/parent/1234/child', 'GET', params=None)

    @patch('gapipy.request.APIRequestor.list_raw')
    def test_list_generator(self, mock_list, mock_request):
        mock_list.side_effect = [FIRST_PAGE_LIST_DATA, SECOND_PAGE_LIST_DATA]
        expected_calls = [
            call(None),
            call('http://localhost:5000/resources/?page=2'),
        ]

        requestor = APIRequestor(self.client, 'resources')
        resources = list(requestor.list())

        self.assertEqual(mock_list.mock_calls, expected_calls)
        self.assertEqual(len(resources), 6)
