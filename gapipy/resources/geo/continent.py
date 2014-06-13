from __future__ import unicode_literals

from ..base import Resource
from .place import Place


class Continent(Resource):

    _resource_name = 'continents'

    _as_is_fields = [
        'id', 'href', 'name',
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _resource_fields = [
        ('place', Place),
    ]
