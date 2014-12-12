from .base import BaseModel

class Room(BaseModel):
    _as_is_fields = ['code', 'name']

class AdvertisedDeparture(BaseModel):
    _as_is_fields = ["previous_amount", "currency", "amount"]
    _model_fields = [
        ('room', Room),
    ]

    @property
    def _resource_fields(self):
        # Import loop
        from ..resources import Departure, Promotion
        return [
            ('departure', Departure),
            ('promotion', Promotion),
        ]
