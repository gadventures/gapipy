from gapipy.resources.base import Resource
from gapipy.models import DossierFeatureParent, DossierFeatureChild


class DossierFeature(Resource):
    _resource_name = 'dossier_features'
    _as_is_fields = [
        'id',
        'href',
        'label',
        'code',
        'description',
        'publish_state',
    ]

    _model_fields = [
        ('parent', DossierFeatureParent),
    ]

    _model_collection_fields = [
        ('children', DossierFeatureChild),
    ]
