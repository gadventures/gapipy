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

    def test_list_resource(self, mock_request):
        requestor = APIRequestor(self.client, 'resources')
        requestor.list_raw()
        mock_request.assert_called_once_with('/resources', 'GET', options=None)

    def test_list_resource_with_parent(self, mock_request):
        parent = ('parent', '1234')
        requestor = APIRequestor(self.client, 'child', parent=parent)
        requestor.list_raw()
        mock_request.assert_called_once_with(
            '/parent/1234/child', 'GET', options=None)

    @patch('gapipy.request.APIRequestor.list_raw')
    def test_list_generator(self, mock_list, mock_request):
        mock_list.side_effect = [FIRST_PAGE_LIST_DATA, SECOND_PAGE_LIST_DATA]
        expected_calls = [
            call(None),
            call('http://localhost:5000/resources/?page=2'),
        ]

        requestor = APIRequestor(self.client, 'resource')
        resources = list(requestor.list())

        self.assertEqual(mock_list.mock_calls, expected_calls)
        self.assertEqual(len(resources), 6)
