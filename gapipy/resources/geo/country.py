from __future__ import unicode_literals

from ..base import Resource
from .state import State


class Country(Resource):

    _resource_name = 'countries'
    _is_parent_resource = True

    _as_is_fields = ['id', 'href', 'name']
    _resource_collection_fields = [('states', State)]
