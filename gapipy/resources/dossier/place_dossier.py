from __future__ import unicode_literals

from ...models.base import BaseModel
from ..base import Resource


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

    _resource_fields = [
        ('place', 'Place')
    ]

    _model_collection_fields = [
        ('details', PlaceDossierDetail),
        ('images', PlaceDossierImage),  # TODO: replace with Image resource
    ]
