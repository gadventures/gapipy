# Python 2 and 3

from .base import Resource


class BookingCompany(Resource):

    _resource_name = 'booking_companies'

    _as_is_fields = [
        'id',
        'href',
        'name',
    ]
    _date_time_fields_utc = ['date_last_modified']
