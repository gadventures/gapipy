from ..base import Resource, BaseModel

from .service import Service


class Requirement(BaseModel):
    _as_is_fields = ['code']


class Override(Resource):
    _resource_name = 'overrides'

    _as_is_fields = [
        'id',
        'href',
    ]

    @property
    def _resource_fields(self):
        from .booking import Booking
        from .customer import Customer
        from .override_reason import OverrideReason

        return [
            ('customer', Customer),
            ('booking', Booking),
            ('reason', OverrideReason),
        ]

    _model_collection_fields = [
        ('services', Service),
    ]

    _model_fields = [
        ('requirement', Requirement),
    ]
