from .base import BaseModel


class IncompleteRequirement(BaseModel):
    _as_is_fields = ['type', 'name', 'code', 'message', 'flags', 'details']

    @property
    def _resource_fields(self):
        from gapipy.resources import Customer
        return [
            ('customer', Customer),
        ]
