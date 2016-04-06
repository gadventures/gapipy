from __future__ import unicode_literals

from ..base import Resource
from ...utils import enforce_string_type


class State(Resource):

    _resource_name = 'states'

    _as_is_fields = ['id', 'href', 'name']
    _resource_fields = [('country', 'Country')]

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
