from __future__ import unicode_literals

from ..base import Resource
from ...models.base import BaseModel


class AccommodationDossier(Resource):
    _resource_name = 'accommodation_dossiers'

    _as_is_fields = [
        'id', 'href', 'name',
        'website',
        'property_type',
        # punt:
        'address',
        'details',
        'features',
        'emails',
        'phone_numbers',
        'rooms',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    @property
    def _model_fields(self):
        from ..geo import Place
        return [
            ('location', Place),
        ]
