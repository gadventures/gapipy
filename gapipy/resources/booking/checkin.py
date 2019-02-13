# Python 2 and 3
from __future__ import unicode_literals

from gapipy.resources.base import Resource
from gapipy.models.base import BaseModel


class Requirement(BaseModel):
    _as_is_fields = ['code']


class RequirementSet(BaseModel):
    _as_is_fields = ['name', 'code']
    _model_collection_fields = [
        ('COMPLETE', Requirement),
        ('INCOMPLETE', Requirement),
    ]


class Checkin(Resource):
    _resource_name = 'checkins'
    _is_listable = True

    _as_is_fields = [
        'id',
        'href',
        'status',
    ]

    _date_fields = ['expires']
    _resource_fields = [
        ('booking', 'Booking'),
        ('customer', 'Customer'),
    ]

    _model_collection_fields = [
        ('requirements', RequirementSet),
    ]
