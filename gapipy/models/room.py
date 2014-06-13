from .add_on import AddOn
from .price_band import PriceBand, SeasonalPriceBand
from .base import BaseModel


class Room(BaseModel):
    _as_is_fields = ['availability', 'code', 'name']

    @property
    def _model_collection_fields(self):
        return [('price_bands', PriceBand)]

    def __repr__(self):
        return '<{0} ({1})>'.format(self.__class__.__name__, self.name)


class AccommodationRoom(Room):
    model_collection_fields = [('price_bands', SeasonalPriceBand)]

    @property
    def _as_is_fields(self):
        return super(AccommodationRoom, self)._as_is_fields + [
            'room_class',
            'max_nights',
            'min_nights',
        ]

    def __init__(self, data):
        super(AccommodationRoom, self).__init__(data)

        # `class` is a reserved word in python
        setattr(self, 'room_class', data['class'])


class DepartureRoom(Room):
    @property
    def _as_is_fields(self):
        return super(DepartureRoom, self)._as_is_fields + [
            'flags',
        ]

    @property
    def _model_collection_fields(self):
        return super(DepartureRoom, self)._model_fields + [
            ('add_ons', AddOn),
        ]
