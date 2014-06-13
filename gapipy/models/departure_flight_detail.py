from .base import BaseModel


class DepartureFlightDetail(BaseModel):
    _as_is_fields = ['departure_flight_number']
    _date_time_fields_local = ['departure_flight_date_time']

    @property
    def _resource_fields(self):
        from gapipy.resources import Customer
        return [
            ('customer', Customer),
        ]
