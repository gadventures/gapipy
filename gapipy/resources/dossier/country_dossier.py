from __future__ import unicode_literals

from ..base import Resource
from .details import DossierDetail
from .dossier_features import DossierFeature


class CountryDossier(Resource):
    _resource_name = 'country_dossiers'

    _as_is_fields = [
        'id', 'href', 'name', 'type',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']

    _resource_fields = [
        ('country', 'Country'),
        ('dossier_segment', 'DossierSegment'),
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
        ('features', DossierFeature),
    ]
