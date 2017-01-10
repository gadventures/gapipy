

from ...models.base import BaseModel
from ..base import Resource

class ServiceLevel(Resource):
    _resource_name = 'service_levels'

    _as_is_fields = [
        'id', 'href', 'code',
        'label',
        'description',
    ]
