# Python 2 and 3
from __future__ import unicode_literals

from gapipy.resources.base import Resource
from gapipy.utils import enforce_string_type

from .country import Country


class Nationality(Resource):

    _resource_name = 'nationalities'

    _as_is_fields = [
        'id',
        'href',
        'name',
    ]

    _resource_fields = [
        ('country', Country),
    ]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
