from __future__ import unicode_literals

from ..base import Resource

from .agency import Agency


class Agent(Resource):
    _resource_name = 'agents'
    _is_listable = False

    _as_is_fields = [
        'id', 'href', 'role', 'first_name', 'last_name', 'email',
        'phone_numbers', 'username', 'active',
    ]
    _resource_fields = [('agency', Agency)]
