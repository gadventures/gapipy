from __future__ import unicode_literals

from ..base import BaseModel, Resource

from .agency import Agency


class AgentRole(BaseModel):
    _as_is_fields = ['id', 'name']


class AgentPhoneNumber(BaseModel):
    _as_is_fields = ['number', 'type']


class Agent(Resource):
    _resource_name = 'agents'
    _is_listable = False

    _as_is_fields = [
        'id',
        'href',
        'first_name',
        'last_name',
        'email',
        'username',
        'active',
    ]
    _model_fields = [
        ('role', AgentRole),
    ]
    _model_collection_fields = [
        ('phone_numbers', AgentPhoneNumber),
    ]
    _resource_fields = [('agency', Agency)]
