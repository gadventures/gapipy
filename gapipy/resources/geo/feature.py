from __future__ import unicode_literals

from ..base import Resource
from .feature_category import FeatureCategory


class Feature(Resource):

    _resource_name = 'features'

    _as_is_fields = [
        'id', 'href', 'name', 'code', 'description',
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
    _resource_fields = [
        ('feature_category', FeatureCategory),
    ]
