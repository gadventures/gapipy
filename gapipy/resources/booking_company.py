# Python 2 and 3
from __future__ import unicode_literals

from .base import Resource


class BookingCompany(Resource):

    _resource_name = 'booking_companies'

    _as_is_fields = [
        'id',
        'href',
        'name',
    ]
