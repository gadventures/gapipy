from __future__ import unicode_literals

from ..base import Resource
from .details import DossierDetail, DossierDetailsMixin


class TransportDossier(Resource, DossierDetailsMixin):
    _resource_name = 'transport_dossiers'

    _as_is_fields = [
        'id', 'href', 'features', 'capacity', 'private', 'name',
        'dossier_segment',
    ]

    _model_collection_fields = [
        ('details', DossierDetail),
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']
