from __future__ import unicode_literals

from .base import Resource


class Language(Resource):

    _resource_name = 'languages'

    _as_is_fields = ['id', 'href', 'name', 'iso_639_3', 'iso_639_1']

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
