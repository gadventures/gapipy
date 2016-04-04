from __future__ import unicode_literals

from ..base import Resource
from ...utils import enforce_string_type


class Nationality(Resource):

    _resource_name = 'nationalities'

    _as_is_fields = ['id', 'href', 'name']

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
