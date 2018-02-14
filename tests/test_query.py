import json
import sys
import unittest

from mock import MagicMock, patch
from requests import HTTPError, Response

from gapipy.client import Client
from gapipy.query import Query
from gapipy.resources import Activity, Departure, Tour, TourDossier
from gapipy.resources.base import Resource
from gapipy.utils import get_available_resource_classes

from .fixtures import (
    PPP_TOUR_DATA, TOUR_DOSSIER_LIST_DATA, DUMMY_DEPARTURE, DUMMY_PROMOTION,
)


class QueryKeyTestCase(unittest.TestCase):

    def setUp(self):
        # Any ol' resource will do.
        self.client = Client(application_key='test_abcd')
        self.resource = get_available_resource_classes()[0]
        self.resource_name = self.resource._resource_name

    def test_query_key_with_env_test(self):
        client = Client(application_key='test_abcd')
        output = client.tour_dossiers.query_key(123)
        expected = 'tour_dossiers:123:test'
        self.assertEqual(output, expected)

    def test_query_key_test(self):
        client = Client(application_key='test')
        output = client.tour_dossiers.query_key(123)
        expected = 'tour_dossiers:123'
        self.assertEqual(output, expected)

    def test_query_key_test_with_no_underscore_with_test(self):
        client = Client(application_key='testringnounderscore')
        output = client.tour_dossiers.query_key(123)
        expected = 'tour_dossiers:123'
        self.assertEqual(output, expected)

    def test_query_key_with_no_underscore(self):
        client = Client(application_key='somestringnounderscore')
        output = client.tour_dossiers.query_key(123)
        expected = 'tour_dossiers:123'
        self.assertEqual(output, expected)

    def test_query_key_with_underscore_live(self):
        client = Client(application_key='live_abs')
        output = client.tour_dossiers.query_key(123)
        expected = 'tour_dossiers:123'
        self.assertEqual(output, expected)

    def test_query_key_with_env_with_language(self):
        self.client = Client(application_key='test_abcd')
        self.client.api_language = 'de'
        output = self.client.tour_dossiers.query_key(123)
        expected = 'tour_dossiers:123:de:test'
        self.assertEqual(output, expected)

    def test_query_key_with_env_with_both_ids(self):
        client = Client(application_key='test_abcd')
        output = client.tour_dossiers.query_key(1, 2)
        expected = 'tour_dossiers:1:2:test'
        self.assertEqual(output, expected)

    def test_query_key_with_env_with_one_id(self):
        client = Client(application_key='test_abcd')
        output = client.tour_dossiers.query_key(1)
        expected = 'tour_dossiers:1:test'
        self.assertEqual(output, expected)

    def test_query_key_with_language(self):
        self.client = Client(application_key='')
        self.client.api_language = 'de'
        query = Query(self.client, self.resource)
        key = query.query_key(1)
        expected = '{}:1:de'.format(self.resource_name)
        self.assertEqual(key, expected)

        # Unsetting the language should also remove it from the key
        self.client.api_language = None
        key = query.query_key(1)
        expected = '{}:1'.format(self.resource_name)
        self.assertEqual(key, expected)

    def test_query_key_with_variation_id(self):
        query = Query(self.client, self.resource)
        key = query.query_key(1, 2)
        expected = '{}:1:2:test'.format(self.resource_name)
        self.assertEqual(key, expected)

    def test_query_key_no_resource_id(self):
        query = Query(self.client, self.resource)
        key = query.query_key()
        self.assertEqual(key, self.resource_name)


class QueryTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.cache = self.client._cache
        self.cache.clear()

    @patch('gapipy.request.APIRequestor._request', return_value=PPP_TOUR_DATA)
    def test_get_instance_by_id(self, mock_request):
        query = Query(self.client, Tour)
        t = query.get(1234)
        self.assertIsInstance(t, Tour)

    @patch('gapipy.request.APIRequestor._request')
    def test_get_instance_with_forbidden_id(self, mock_request):
        response = Response()
        response.status_code = 403
        http_error = HTTPError(response=response)
        mock_request.side_effect = http_error

        query = Query(self.client, Tour)
        t = query.get(1234)
        self.assertIsNone(t)

    @patch('gapipy.request.APIRequestor._request')
    def test_get_instance_with_non_existing_id(self, mock_request):
        response = Response()
        response.status_code = 404
        http_error = HTTPError(response=response)
        mock_request.side_effect = http_error

        query = Query(self.client, Tour)
        t = query.get(1234)
        self.assertIsNone(t)

    @patch('gapipy.request.APIRequestor._request')
    def test_get_instance_with_gone_id(self, mock_request):
        response = Response()
        response.status_code = 410
        http_error = HTTPError(response=response)
        mock_request.side_effect = http_error

        query = Query(self.client, Tour)
        t = query.get(1234)
        self.assertIsNone(t)

    @patch('gapipy.request.APIRequestor._request')
    def test_get_instance_by_id_with_non_404_error(self, mock_request):
        response = Response()
        response.status_code = 401
        http_error = HTTPError(response=response)
        mock_request.side_effect = http_error

        query = Query(self.client, Tour)
        with self.assertRaises(HTTPError) as cm:
            query.get(1234)

        self.assertEqual(cm.exception.response.status_code, 401)

    @patch('gapipy.request.APIRequestor._request')
    def test_filtered_query(self, mock_request):
        """
        Arguments passed to .filter() are stored on the Query instance but are
        cleared when that query is evaluated.
        """
        # Create a basic filter query for PPP...
        query = Query(self.client, Tour).filter(tour_dossier_code='PPP')
        self.assertEqual(len(query._filters), 1)

        # ... then chain on another filter argument...
        query = query.filter(order_by__asc='departures_start_date')
        self.assertEqual(len(query._filters), 2)

        # ... and force query evaluation, before checking...
        list(query)

        # ... our request was made with the appropriate query args, and...
        mock_request.assert_called_once_with(
            '/tours', 'GET', params={
                'tour_dossier_code': 'PPP',
                'order_by__asc': 'departures_start_date',
            })
        mock_request.reset_mock()

        # ... our stored filter args got reset.
        self.assertEqual(len(query._filters), 0)

        # Check .count() also clears stored filter args appropriately:
        query.filter(
            tour_dossier_code='PPP',
            order_by__desc='departures_start_date').count()
        mock_request.assert_called_once_with(
            '/tours', 'GET', params={
                'tour_dossier_code': 'PPP',
                'order_by__desc': 'departures_start_date',
            })
        mock_request.reset_mock()
        self.assertEqual(len(query._filters), 0)


    @patch('gapipy.request.APIRequestor._request')
    def test_query_reset_filter(self, mock_request):
        query = Query(self.client, Tour)
        query.filter(tour_dossier_code='PPP').count()
        self.assertEqual(query._filters, {})

    def test_listing_non_listable_resource_fails(self):
        message = 'The Activity resource is not listable and/or is only available as a subresource'
        if sys.version_info.major < 3:
            with self.assertRaisesRegexp(ValueError, message):
                Query(self.client, Activity).all()
            with self.assertRaisesRegexp(ValueError, message):
                Query(self.client, Activity).count()
        else:
            with self.assertRaisesRegex(ValueError, message):
                Query(self.client, Activity).all()
            with self.assertRaisesRegex(ValueError, message):
                Query(self.client, Activity).count()

    @patch('gapipy.request.APIRequestor._request', return_value=DUMMY_PROMOTION)
    def test_can_retrieve_single_non_listable_resource(self, mock_request):
        Query(self.client, Activity).get(1234)
        mock_request.assert_called_once_with(
            '/activities/1234', 'GET', additional_headers=None)

    @patch('gapipy.request.APIRequestor._request', return_value=DUMMY_DEPARTURE)
    def test_can_retrieve_single_subresource_without_parent(self, mock_request):
        Query(self.client, Departure).get(1234)
        mock_request.assert_called_once_with(
            '/departures/1234', 'GET', additional_headers=None)

    @patch('gapipy.request.APIRequestor._request', return_value=TOUR_DOSSIER_LIST_DATA)
    def test_count(self, mock_request):
        query = Query(self.client, TourDossier)
        count = query.count()
        self.assertIsInstance(count, int)
        self.assertEqual(count, 3)

    @patch('gapipy.request.APIRequestor._request', return_value=TOUR_DOSSIER_LIST_DATA)
    def test_fetch_all(self, mock_request):

        query = Query(self.client, TourDossier).all()
        self.assertFalse(mock_request.called)

        dossiers = list(query)
        self.assertTrue(mock_request.called)

        self.assertEqual(len(dossiers), 3)
        for dossier in dossiers:
            self.assertIsInstance(dossier, TourDossier)

        mock_request.assert_called_once_with(
            '/tour_dossiers', 'GET', params={})

    @patch('gapipy.request.APIRequestor._request', return_value=TOUR_DOSSIER_LIST_DATA)
    def test_fetch_all_with_limit(self, mock_request):

        query = Query(self.client, TourDossier).all(limit=2)
        dossiers = list(query)

        self.assertEqual(len(dossiers), 2)
        for dossier in dossiers:
            self.assertIsInstance(dossier, TourDossier)

        mock_request.assert_called_once_with(
            '/tour_dossiers', 'GET', params={})

    def test_fetch_all_with_wrong_argument_for_limit(self):
        message = '`limit` must be a positive integer'
        if sys.version_info.major < 3:
            with self.assertRaisesRegexp(ValueError, message):
                query = Query(self.client, Tour).all(limit=-1)
                list(query)  # force the query to evaluate
        else:
            with self.assertRaisesRegex(ValueError, message):
                query = Query(self.client, Tour).all(limit=-1)
                list(query)  # force the query to evaluate


class QueryCacheTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(cache_backend='gapipy.cache.SimpleCache')
        self.cache = self.client._cache
        self.cache.clear()

    @patch('gapipy.request.APIRequestor._request', return_value=PPP_TOUR_DATA)
    def test_resources_are_cached(self, mock_request):
        query = Query(self.client, Tour)

        self.assertEqual(self.cache.count(), 0)

        query.get(21346)
        self.assertEqual(self.cache.count(), 1)
        self.assertEqual(len(mock_request.mock_calls), 1)

        query.get(21346)
        self.assertEqual(len(mock_request.mock_calls), 1)

    def test_cached_get_does_not_set(self):
        """
        Regression test https://github.com/gadventures/gapipy/issues/65

        We discovered that when getting a resource, even if it is a hit in our
        local cache we would set the data back into our cache every time. When
        using a cache with a TTL on keys (e.g. Redis) this has the effect of
        resetting the TTL each time that that key is retrieved. This is not the
        expected behaviour wrt cache key TTLs.
        """
        query = Query(self.client, Tour)

        # act like we already have the data in our cache
        mock_cache_get = MagicMock(return_value=PPP_TOUR_DATA)
        self.cache.get = mock_cache_get

        mock_cache_set = MagicMock()
        self.cache.set = mock_cache_set

        query.get(21346)
        self.assertEqual(len(mock_cache_get.mock_calls), 1)
        self.assertEqual(len(mock_cache_set.mock_calls), 0)


class MockResource(Resource):
    _as_is_fields = ['id', 'first_name', 'last_name']
    _resource_name = 'mocks'


@patch('gapipy.request.APIRequestor._request')
class UpdateCreateResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_object_accessor(self, mock_request):
        data = {'first_name': 'Jon', 'last_name': 'Ive', 'id': None}
        r = MockResource(data, client=self.client)
        self.assertEqual(r.first_name, data['first_name'])

    def test_object_attr_modify(self, mock_request):
        data = {'first_name': 'Jon', 'last_name': 'Ive', 'id': None}
        r = MockResource(data, client=self.client)
        r.first_name = 'Jonathan'
        self.assertEqual(r.first_name, 'Jonathan')

    def test_create_object(self, mock_request):
        data = {
            'first_name': 'Jon',
            'last_name': 'Ive',
            'id': None,
        }
        # modify mock_request to return a value
        # this is needed for save -> _fill_fields
        mock_request.return_value = data

        r = MockResource(data, client=self.client)
        r.save()
        mock_request.assert_called_once_with(
            '/mocks', 'POST', data=r.to_json())

    def test_update_object(self, mock_request):
        data = {
            'first_name': 'Jon',
            'last_name': 'Ive',
            'id': 1,
        }
        # modify mock_request to return a value
        # this is needed for save -> _fill_fields
        mock_request.return_value = {
            'id': 1,
            'first_name': 'Jonathan',
            'last_name': 'Ive',
        }

        r = MockResource(data, client=self.client)
        r.first_name = 'Jonathan'
        r.save()

        mock_request.assert_called_once_with(
            '/mocks/1', 'PUT', data=r.to_json())

    def test_partial_update_object(self, mock_request):
        data = {
            'first_name': 'Jon',
            'last_name': 'Ive',
            'id': 1,
        }
        mock_request.return_value = data
        r = MockResource(data, client=self.client)

        r.first_name = 'Jonathan'
        r_data = {
            'first_name': 'Jonathan',
            'last_name': 'Ive',
            'id': 1
        }
        mock_request.return_value = r_data
        r.save(partial=True)
        changed = {'first_name': 'Jonathan'}
        mock_request.assert_called_once_with(
            '/mocks/1', 'PATCH', data=json.dumps(changed))
        self.assertEqual(r.to_dict(), r_data)

        r.last_name = 'Ivey'
        r_data = {
            'first_name': 'Jonathan',
            'last_name': 'Ivey',
            'id': 1,
        }
        mock_request.return_value = r_data
        r.save(partial=True)
        changed = {'last_name': 'Ivey'}
        mock_request.assert_called_with(
            '/mocks/1', 'PATCH', data=json.dumps(changed))
        self.assertEqual(r.to_dict(), r_data)
