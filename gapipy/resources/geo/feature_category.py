from __future__ import unicode_literals

from ..base import Resource


class FeatureCategory(Resource):

    _resource_name = 'feature_categories'

    _as_is_fields = [
        'id', 'href', 'code', 'description',
    ]
    _date_time_fields_utc = ['date_created', 'date_last_modified']
