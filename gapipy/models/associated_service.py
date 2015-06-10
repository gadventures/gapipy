from .base import BaseModel

class AssociatedService(BaseModel):
    """
    Represent an associated service. Each service can be associated
    to other services within the same booking.
    """
    _as_is_fields = ['id', 'href']
