from .addon import AddOn
from .price_band import PriceBand, SeasonalPriceBand
from .base import BaseModel
from ..utils import enforce_string_type


class Room(BaseModel):
    _as_is_fields = ['availability', 'code', 'name']

    @property
    def _model_collection_fields(self):
        return [('price_bands', PriceBand)]

    @enforce_string_type
    def __repr__(self):
        return '<{0} ({1})>'.format(self.__class__.__name__, self.name)


class AccommodationRoom(Room):

    @property
    def _as_is_fields(self):
        return super(AccommodationRoom, self)._as_is_fields + [
            'room_class',
            'max_nights',
            'min_nights',
        ]

    @property
    def _model_collection_fields(self):
        return [('price_bands', SeasonalPriceBand)]

    def __init__(self, data, **kwargs):
        super(AccommodationRoom, self).__init__(data, **kwargs)

        # `class` is a reserved word in python, so we instead use `room_class`
        # as the attribute for the room class.

        room_class = data.get('class')
        if room_class is None:
            # Sometimes, the data we receive comes from `gapipy` (for example,
            # if local caching is used), so the info we need is already at the
            # `room_class` key.
            room_class = data.get('room_class')

        setattr(self, 'room_class', room_class)


class DepartureRoom(Room):
    @property
    def _as_is_fields(self):
        return super(DepartureRoom, self)._as_is_fields + [
            'flags',
        ]

    @property
    def _model_collection_fields(self):
        return super(DepartureRoom, self)._model_collection_fields + [
            ('addons', AddOn),
        ]
