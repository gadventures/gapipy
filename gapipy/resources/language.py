from __future__ import unicode_literals

from .base import Resource
from ..utils import enforce_string_type


class Language(Resource):

    _resource_name = 'languages'

    _as_is_fields = ['id', 'href', 'name', 'iso_639_3', 'iso_639_1']

    @enforce_string_type
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
