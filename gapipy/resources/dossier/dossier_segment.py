from __future__ import unicode_literals

from ..base import Resource
from ...models import DossierFeatureParent, DossierFeatureChild


class DossierSegment(Resource):
    _resource_name = 'dossier_segments'
    _as_is_fields = ['id', 'href', 'label', 'code', 'description']

    _model_fields = [
        ('parent', DossierFeatureParent),
    ]

    _model_collection_fields = [
        ('children', DossierFeatureChild),
    ]
