from __future__ import unicode_literals

from ..base import Resource
from .place import Place


class Airport(Resource):

    _resource_name = 'airports'

    _as_is_fields = [
        'id', 'href', 'name', 'iata_code', 'icao_code', 'active'
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _resource_fields = [
        ('place', Place),
        ('city', Place),
    ]
