from __future__ import unicode_literals

from ..base import Resource
from ...models.base import BaseModel

class PlaceDossierImage(BaseModel):
    _as_is_fields = ['id', 'href', 'date_created', 'date_last_modified']

class PlaceDossierDetailType(BaseModel):
    _as_is_fields = ['code', 'label', 'description']

class PlaceDossierDetail(BaseModel):
    _as_is_fields = ['body']

    _model_fields = [
        ('detail_type', PlaceDossierDetailType),
    ]

class PlaceDossier(Resource):
    _resource_name = 'place_dossiers'

    _as_is_fields = [
        'id', 'href', 'name'
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    _model_collection_fields = [
        ('details', PlaceDossierDetail),
        ('images', PlaceDossierImage),
    ]

    @property
    def _model_fields(self):
        from ..geo import Place
        return [
            ('place', Place)
        ]
