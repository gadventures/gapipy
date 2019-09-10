# Python 2 and 3
from __future__ import unicode_literals

from gapipy.models.base import BaseModel
from gapipy.resources.base import Resource
from gapipy.utils import get_resource_class_from_resource_name

from .service import Service


class LastModified(BaseModel):
    _as_is_fields = [
        'name',
        'user_type',
    ]
    _date_time_fields_utc = ['date']


class ResourceField(BaseModel):
    _as_is_fields = [
        'field',
        'required',
        'value',
        'viewable_by',
    ]

    @property
    def _resource_fields(self):
        # extract the resource_name from the raw data
        # and use it to return the appropriate resource
        # class
        resource_name = self._raw_data.get('resource', {}).get('resource_name')
        if resource_name:
            try:
                resource_class = get_resource_class_from_resource_name(resource_name)
                return [
                    ('resource', resource_class),
                ]
            except:
                pass
        # fall back
        return []


class Requirement(Resource):
    _resource_name = 'requirements'

    _as_is_fields = [
        'id',
        'href',
        'type',
        'applied_overrides',
        'code',
        'editable_by',
        'flags',
        'name',
        'override_reasons',
        'status',
    ]

    _date_fields = [
        'complete_by_date',
    ]

    _model_fields = [
        ('last_modified', LastModified),
    ]

    _resource_fields = [
        ('booking', 'Booking'),
        ('customer', 'Customer'),
        ('requirement_set', 'RequirementSet'),
    ]

    _model_collection_fields = [
        ('services', Service),
        ('resource_fields', ResourceField),
    ]


class RequirementSet(Resource):
    _resource_name = 'requirement_sets'

    _is_listable = True

    _as_is_fields = [
        'id',
        'href',
        'code',
        'name',
    ]

    _date_fields = [
        'complete_by_date',
    ]

    _model_collection_fields = [
        ('requirements', Requirement),
    ]

    _resource_fields = [
        ('booking', 'Booking'),
    ]

