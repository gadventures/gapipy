from __future__ import unicode_literals

from ..base import Resource


class Nationality(Resource):

    _resource_name = 'nationalities'

    _as_is_fields = ['id', 'href', 'name']

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
