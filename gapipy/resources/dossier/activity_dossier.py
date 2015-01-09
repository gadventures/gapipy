from __future__ import unicode_literals

from ..base import Resource
from ...models.base import BaseModel


class ActivityDossier(Resource):
    _resource_name = 'activity_dossiers'

    _as_is_fields = [
        'id', 'href',
        'name',
        'duration_min', 'duration_max',
        'price_per_person_min', 'price_per_person_max',
        'price_per_group_min', 'price_per_group_max',
        'currency',
        # XXX do we need something else for these two?
        'dossier_segment',
        'details',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    @property
    def _model_fields(self):
        from ..geo import Place
        return [
            ('start_location', Place),
            ('end_location', Place),
        ]
