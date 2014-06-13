from .base import BaseModel


class InternationalTicketNumber(BaseModel):
    _as_is_fields = ['ticket_number']

    @property
    def _resource_fields(self):
        from gapipy.resources import Customer
        return [
            ('customer', Customer),
        ]
