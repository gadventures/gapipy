from __future__ import unicode_literals

from ..base import Resource


class TransportDossier(Resource):
    _resource_name = 'transport_dossiers'

    _as_is_fields = [
        'id', 'href', 'features', 'capacity', 'private', 'name',
        'dossier_segment', 'details',
    ]

    _date_time_fields_local = ['date_created', 'date_last_modified']
