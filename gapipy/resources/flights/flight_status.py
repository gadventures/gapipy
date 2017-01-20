from ..base import Resource

from .flight_segment import FlightSegment


class FlightStatus(Resource):
    _resource_name = 'flight_statuses'

    _as_is_fields = [
        'current_segment',
        'departure_service_action',
        'flags',
        'href',
        'id',
        'internal',
        'segments_order',
        'state',
    ]

    @property
    def _resource_fields(self):
        # Prevent Import Loop
        from ..booking import (
            DepartureService,
            FlightService,
        )

        return [
            ('departure_service', DepartureService),
            ('flight_service', FlightService),
            ('next_status', 'FlightStatus'),
            ('previous_status', 'FlightStatus'),
        ]

    @property
    def _model_collection_fields(self):
        from ..booking import Customer

        return [
            ('customers', Customer),
            ('segments', FlightSegment),
        ]
