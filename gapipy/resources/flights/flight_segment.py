from ..base import Resource, BaseModel


class Airline(BaseModel):
    _as_is_fields = [
        'code',
        'name',
    ]


class Airport(BaseModel):
    _as_is_fields = [
        'code',
        'name',
    ]


class FlightSegment(Resource):
    _as_is_fields = [
        'id',
        'href',
        'state',
        'flight_number',
        'departure_gate',
        'departure_terminal',
        'arrival_terminal',
        'arrival_gate',
    ]

    _model_fields = [
        ('airline', Airline),
        ('arrival_airport', Airport),
        ('departure_airport', Airport),
        ('next_segment', 'FlightSegment'),
        ('previous_segment', 'FlightSegment'),
    ]

    _date_time_fields_utc = [
        'departure_datetime_utc',
        'arrival_datetime_utc',
    ]

    _date_time_fields_local = [
        'departure_datetime_local',
        'arrival_datetime_local',
    ]
