import sys
import unittest

from mock import call, patch

from gapipy.client import Client
from gapipy.models.base import _Parent
from gapipy.request import APIRequestor

from .fixtures import FIRST_PAGE_LIST_DATA, SECOND_PAGE_LIST_DATA


class Resources(object):
    def __init__(self, **kwArgs):
        self.__dict__.update(kwArgs)


class APIRequestorTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.resources = Resources(_resource_name='resources', _uri=None)

    @patch('gapipy.request.APIRequestor._request')
    def test_get_resource_by_id(self, mock_request):
        requestor = APIRequestor(self.client, self.resources)
        requestor.get(1234)
        mock_request.assert_called_once_with('/resources/1234', 'GET', additional_headers=None)

    @patch('gapipy.request.APIRequestor._request')
    def test_get_with_null_resource_id_and_uri_raises_error(self, mock_request):
        requestor = APIRequestor(self.client, self.resources)
        error_msg = 'Need to provide at least one of `resource_id` or `uri` as argument'
        if sys.version_info.major < 3:
            with self.assertRaisesRegexp(ValueError, error_msg):
                requestor.get()
        else:
            with self.assertRaisesRegex(ValueError, error_msg):
                requestor.get()

    @patch('gapipy.request.APIRequestor._request')
    def test_get_with_falsy_resource_id_does_not_raise_error(self, mock_request):
        requestor = APIRequestor(self.client, self.resources)
        requestor.get(0)
        mock_request.assert_called_once_with('/resources/0', 'GET', additional_headers=None)

    @patch('gapipy.request.APIRequestor._request')
    def test_list_resource(self, mock_request):
        requestor = APIRequestor(self.client, self.resources)
        requestor.list_raw()
        mock_request.assert_called_once_with('/resources', 'GET', params=None)

    @patch('gapipy.request.APIRequestor._request')
    def test_list_raw_uri_requestor_params(self, mock_request):
        params = {'param': 'value'}
        requestor = APIRequestor(self.client, self.resources, params=params)
        requestor.list_raw('/test_uri')
        mock_request.assert_called_once_with('/test_uri', 'GET', params=params)

    @patch('gapipy.request.APIRequestor._request')
    def test_list_raw_uri_no_requestor_params(self, mock_request):
        requestor = APIRequestor(self.client, self.resources)
        requestor.list_raw('/test_uri')
        mock_request.assert_called_once_with('/test_uri', 'GET', params=None)

    @patch('gapipy.request.APIRequestor._request')
    def test_list_raw_uri_params_requestor_params(self, mock_request):
        params = {'param': 'value'}
        requestor = APIRequestor(self.client, self.resources, params=params)
        requestor.list_raw('/test_uri?')
        mock_request.assert_called_once_with('/test_uri?', 'GET', params=params)

    @patch('gapipy.request.APIRequestor._request')
    def test_list_raw_uri_params_no_requestor_params(self, mock_request):
        requestor = APIRequestor(self.client, self.resources)
        requestor.list_raw('/test_uri?')
        mock_request.assert_called_once_with('/test_uri?', 'GET', params=None)

    @patch('gapipy.request.APIRequestor._request')
    def test_list_resource_with_parent(self, mock_request):
        parent = _Parent('parent', '1234', None)
        requestor = APIRequestor(self.client, self.resources, parent=parent)
        requestor.list_raw()
        mock_request.assert_called_once_with(
            '/parent/1234/resources', 'GET', params=None)

    @patch('gapipy.request.APIRequestor.list_raw')
    def test_list_generator(self, mock_list):
        mock_list.side_effect = [FIRST_PAGE_LIST_DATA, SECOND_PAGE_LIST_DATA]
        expected_calls = [
            call(None),
            call('http://localhost:5000/resources/?page=2'),
        ]

        requestor = APIRequestor(self.client, self.resources)
        resources = list(requestor.list())

        self.assertEqual(mock_list.mock_calls, expected_calls)
        self.assertEqual(len(resources), 6)

    @patch('gapipy.request.APIRequestor._request')
    def test_uuid_not_set(self, mock_request):
        self.client.uuid = False
        requestor = APIRequestor(self.client, self.resources)
        requestor.params = {'test': '1234'}
        requestor.list_raw()
        mock_request.assert_called_once_with('/resources', 'GET', params={'test': '1234'})

    @patch('gapipy.request.APIRequestor._make_call')
    def test_uuid_set(self, mock_make_call):
        self.client.uuid = True
        requestor = APIRequestor(self.client, self.resources)
        requestor.list_raw()
        params_arg = mock_make_call.call_args[0][-1]
        self.assertTrue('uuid' in params_arg)

    @patch('gapipy.request.APIRequestor._make_call')
    def test_uuid_with_other_params(self, mock_make_call):
        self.client.uuid = True
        requestor = APIRequestor(self.client, self.resources)
        requestor.params = {'test': '1234'}
        requestor.list_raw()
        params_arg = mock_make_call.call_args[0][-1]
        self.assertEqual(params_arg['test'], '1234')
        self.assertTrue('uuid' in params_arg)

    def test_extra_headers_from_client(self):
        """
        The client's "extra_http_headers" should be included when generating
        HTTP headers for a request.
        """
        header_name = "x-farnsworth"
        header_value = "here's where I keep assorted lengths of wire",
        self.client.extra_http_headers = {header_name: header_value}
        requestor = APIRequestor(self.client, self.resources)

        method = 'METHOD'
        additional_headers = {}
        request_headers = requestor._get_headers(method, additional_headers)

        self.assertIn(header_name, request_headers)
        self.assertEqual(request_headers[header_name], header_value)

    def test_extra_headers_from_client_overriden_by_additional_headers(self):
        """
        The client's "extra_http_headers" should be included when generating
        HTTP headers for a request, but are overridable by headers added later.
        """
        header_name = "x-farnsworth"
        header_value = "here's where I keep assorted lengths of wire",
        self.client.extra_http_headers = {header_name: header_value}
        requestor = APIRequestor(self.client, self.resources)

        method = 'METHOD'

        # If `_get_headers` is given an `additional_headers` value with the
        # same `header_name` as was in the client configs...
        request_headers = requestor._get_headers(method, {
            header_name: 'good news'
        })

        # ... the value from `additional_headers` will be the one in the final
        # header-dict
        self.assertIn(header_name, request_headers)
        self.assertEqual(request_headers[header_name], 'good news')
