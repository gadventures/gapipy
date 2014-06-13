from .base import BaseModel


class DepartureServiceRoom(BaseModel):
    _as_is_fields = ['name', 'code']

    @property
    def _resource_fields(self):
        from gapipy.resources import Customer
        return [
            ('customers', Customer),
        ]
