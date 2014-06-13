import datetime
from unittest import TestCase

from mock import patch

from gapipy.query import Query
from gapipy.models import DATE_FORMAT
from gapipy.resources import Tour, TourDossier
from gapipy.resources.base import Resource

from .fixtures import PPP_TOUR_DATA, PPP_DOSSIER_DATA


class ResourceTestCase(TestCase):

    def test_to_dict(self):
        t = Tour(PPP_TOUR_DATA)
        self.assertEquals(t.to_dict(), PPP_TOUR_DATA)

    def test_to_dict_datetimes(self):
        class DatetimeResource(Resource):
            _as_is_fields = ['id']
            _date_fields = ['date_field']
            _date_time_fields_utc = ['date_field_utc']

        resource = DatetimeResource({
            'id': 1,
            'date_field': '2013-02-18',
            'date_field_utc': '2013-02-18T18:17:20Z',
        })
        data = resource.to_dict()
        self.assertEquals(data['date_field'], '2013-02-18')
        self.assertEquals(data['date_field_utc'], '2013-02-18T18:17:20Z')

    @patch('gapipy.request.APIRequestor._request', return_value=PPP_DOSSIER_DATA)
    def test_instantiate_from_raw_data(self, mock_request):
        t = Tour(PPP_TOUR_DATA)
        self.assertIsInstance(t, Tour)
        self.assertEqual(t.product_line, 'PPP')
        self.assertIsInstance(t.departures_start_date, datetime.datetime)
        self.assertIsInstance(t.tour_dossier, TourDossier)
        self.assertIsInstance(t.departures, Query)

    @patch('gapipy.request.APIRequestor._request')
    def test_populate_stub(self, mock_fetch):
        mock_fetch.return_value = {
            'id': 1,
            'product_line': 'PPP',
            'href': '/1',
            'departures_start_date': '2013-01-01',
            'departures_end_date': '2014-01-01',
            'tour_dossier': {
                'id': 1,
            },
            'departures': [
                {'id': 1},
                {'id': 2},
            ],
        }
        data = {'id': 1, 'product_line': 'PPP'}

        t = Tour(data, stub=True)
        self.assertTrue(t.is_stub)
        self.assertEquals(t.id, 1)

        self.assertTrue(isinstance(t.tour_dossier, TourDossier))
        self.assertTrue(isinstance(t.departures, Query))

        # Force a fetch.
        assert t.departures_start_date

        mock_fetch.assert_called_once()
        self.assertFalse(t.is_stub)
        self.assertEquals(
            t.departures_start_date,
            datetime.datetime.strptime('2013-01-01', DATE_FORMAT)
        )
        self.assertEquals(
            t.departures_end_date,
            datetime.datetime.strptime('2014-01-01', DATE_FORMAT)
        )

    def test_model_fields(self):
        from gapipy.models.base import BaseModel

        class Bar(BaseModel):
            _as_is_fields = ['id']
            _date_fields = ['date']

        class Foo(Resource):
            _model_fields = [('bar', Bar)]

        data = {
            'bar': {
                'id': 1,
                'date': '2013-01-01',
            }
        }
        f = Foo(data)

        self.assertEquals(f.to_dict(), {
            'bar': {'id': 1, 'date': '2013-01-01'}
        })
        self.assertIsInstance(f.bar, Bar)
        self.assertEquals(f.bar.id, 1)
        self.assertEquals(f.bar.date, datetime.datetime(2013, 01, 01))
