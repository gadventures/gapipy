# Python 2 and 3
from __future__ import unicode_literals

from ..base import Resource
from .details import DossierDetail, DossierDetailsMixin
from .dossier_features import DossierFeature


class TransportDossier(Resource, DossierDetailsMixin):
    _resource_name = 'transport_dossiers'

    _as_is_fields = [
        'id',
        'href',
        'capacity',
        'private',
        'name',
        'dossier_segment',
        'type',
        'publish_state',
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
        ('features', DossierFeature),
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']
