from .base import BaseModel


class ArrivalFlightDetail(BaseModel):
    _as_is_fields = ['arrival_flight_number']
    _date_time_fields_local = ['arrival_flight_date_time']

    @property
    def _resource_fields(self):
        from gapipy.resources import Customer
        return [
            ('customer', Customer),
        ]
