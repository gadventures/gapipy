from .base import BaseModel


class TravellerHeight(BaseModel):
    _as_is_fields = ['height']

    @property
    def _resource_fields(self):
        from gapipy.resources import Customer
        return [
            ('customer', Customer),
        ]
