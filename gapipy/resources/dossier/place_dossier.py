from __future__ import unicode_literals

from ...models.base import BaseModel
from ..base import Resource
from .details import DossierDetail


class PlaceDossier(Resource):
    _resource_name = 'place_dossiers'

    _as_is_fields = [
        'id', 'href', 'name', 'type',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    _resource_fields = [
        ('place', 'Place')
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
        ('images', 'Image'),
    ]
