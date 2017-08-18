# Python 2 and 3
from __future__ import unicode_literals

from future.utils import with_metaclass

from ...utils import get_resource_class_from_resource_name
from ...models import (
    ArrivalFlightDetail,
    AssociatedService,
    DepartureFlightDetail,
    DepartureServiceRoom,
    DocumentInfo,
    IncompleteRequirement,
    InternationalTicketNumber,
    TravellerHeight,
)

from ..base import Resource, BaseModel

from ..tour import (
    Departure,
    DepartureComponent,
    Accommodation,
    Activity,
    Transport,
    SingleSupplement,
)
from .customer import Customer
from .declined_reason import DeclinedReason


class TypeBasedServiceMeta(type):
    def __call__(cls, *args, **kwargs):
        # Attempt to extract the type from the data. If it's not found for
        # whatever reason, we can't assume what the user was attempting, and
        # we'll simply ignore any metaclass magic.
        resource_name = args[0].get('type', None) if args else None

        if resource_name is None:
            return type.__call__(cls, *args, **kwargs)

        new_class = get_resource_class_from_resource_name(resource_name)
        return type.__call__(new_class, *args, **kwargs)


# with_metaclass is Python 2 and Python 3 method to allow metaclasses
class Service(with_metaclass(TypeBasedServiceMeta, Resource)):
    _resource_name = 'services'
    _is_listable = False
    _is_parent_resource = True

    @property
    def _as_is_fields(self):
        return [
            'id', 'href', 'name', 'status', 'type', 'sub_type', 'flags',
            'applied_promotion',
            'status_transitions',
        ]

    @property
    def _date_fields(self):
        return ['start_date', 'finish_date']

    @property
    def _date_time_fields_utc(self):
        return [
            'date_created', 'date_confirmed',
            'date_cancelled', 'option_expiry_date',
        ]

    @property
    def _date_time_fields_local(self):
        return []

    @property
    def _price_fields(self):
        return [
            'purchase_price', 'commission',
        ]

    @property
    def _resource_fields(self):
        return [
            ('booking', 'Booking'),
            ('declined_reason', DeclinedReason),
        ]

    @property
    def _model_collection_fields(self):
        return [
            ('customers', Customer),
            ('documents', DocumentInfo),
        ]


class ServiceProduct(Service):
    def _get_product(self):
        # Return the appropriate product based on the parent service.
        mapping = {
            'departure_services': Departure,
            'accommodation_services': Accommodation,
            'transport_services': Transport,
            'activity_services': Activity,
            'single_supplement_services': SingleSupplement,
        }
        return mapping[self._resource_name]

    @property
    def _resource_fields(self):
        return super(ServiceProduct, self)._resource_fields + [
            ('product', self._get_product()),
        ]


class Airport(BaseModel):
    _as_is_fields = ['code', 'name']


class Airline(BaseModel):
    _as_is_fields = ['code', 'name']


class FlightServiceSegment(Resource):
    _as_is_fields = [
        'id',
        'href',
        'flight_number',
        'booking_class',
        'technical_stops',
    ]

    _model_fields = [
        ('airline', Airline),
        ('origin_airport', Airport),
        ('destination_airport', Airport),
    ]

    _date_time_fields_local = [
        'departure_date',
        'arrival_date',
    ]

    _resource_fields = [
        ('flight_service', 'FlightService'),
    ]


class DepartureServiceFlight(BaseModel):
    _model_collection_fields = [
        ('flights', FlightServiceSegment)
    ]

    _resource_fields = [
        ('customer', Customer),
    ]


class DepartureService(ServiceProduct):
    _resource_name = 'departure_services'

    @property
    def _price_fields(self):
        return super(DepartureService, self)._price_fields + [
            'deposit',
        ]

    @property
    def _resource_fields(self):
        return (super(DepartureService, self)._resource_fields + [
            ('itinerary', 'Itinerary'),
            ('original_departure_service', DepartureService),
        ])

    @property
    def _resource_collection_fields(self):
        return super(DepartureService, self)._resource_collection_fields + [
            ('components', DepartureComponent),
        ]

    @property
    def _model_collection_fields(self):
        return super(DepartureService, self)._model_collection_fields + [
            ('arrival_flight_details', ArrivalFlightDetail),
            ('departure_flight_details', DepartureFlightDetail),
            ('incomplete_requirements', IncompleteRequirement),
            ('international_ticket_numbers', InternationalTicketNumber),
            ('rooms', DepartureServiceRoom),
            ('arriving_flights', DepartureServiceFlight),
            ('departing_flights', DepartureServiceFlight),
            ('traveller_heights', TravellerHeight),
        ]


class AccommodationService(ServiceProduct):
    _resource_name = 'accommodation_services'

    @property
    def _as_is_fields(self):
        return super(AccommodationService, self)._as_is_fields + [
            'room',
        ]

    @property
    def _model_collection_fields(self):
        return super(AccommodationService, self)._model_collection_fields + [
            ('associated_services', AssociatedService),
        ]


class TransportService(ServiceProduct):
    _resource_name = 'transport_services'

    @property
    def _as_is_fields(self):
        return super(TransportService, self)._as_is_fields + [
            'flight_number', 'pickup_time',
        ]

    @property
    def _model_collection_fields(self):
        return super(TransportService, self)._model_collection_fields + [
            ('associated_services', AssociatedService),
        ]


class ActivityService(ServiceProduct):
    _resource_name = 'activity_services'

    @property
    def _model_collection_fields(self):
        return (super(ActivityService, self)._model_collection_fields + [
            ('arrival_flight_details', ArrivalFlightDetail),
            ('associated_services', AssociatedService),
            ('incomplete_requirements', IncompleteRequirement),
        ])


class SingleSupplementService(ServiceProduct):
    _resource_name = 'single_supplement_services'

    @property
    def _model_collection_fields(self):
        return super(SingleSupplementService, self)._model_collection_fields + [
            ('associated_services', AssociatedService),
        ]


class InsuranceService(Service):
    _resource_name = 'insurance_services'

    @property
    def _as_is_fields(self):
        return super(InsuranceService, self)._as_is_fields + [
            'policy_details_url',
            'policy_number',
            'policy_provider',
            'policy_type',
        ]

    @property
    def _price_fields(self):
        return super(InsuranceService, self)._price_fields + [
            'policy_amount',
            'insurable_amount',
        ]


class FeeService(Service):
    _resource_name = 'fee_services'

    @property
    def _as_is_fields(self):
        return super(FeeService, self)._as_is_fields + [
            'description',
            'related_service',
        ]


class FlightStatus(BaseModel):
    """
    Represent a flight_status attached to the FlightService
    """
    _as_is_fields = ['id', 'href']


class FlightService(Service):
    _resource_name = 'flight_services'

    @property
    def _as_is_fields(self):
        return super(FlightService, self)._as_is_fields + [
            'record_locator',
            'itinerary_url',
            'segments',
        ]

    @property
    def _price_fields(self):
        price_fields = super(FlightService, self)._price_fields

        return [
            field for field in price_fields
            if field not in ('commission', )
        ]

    @property
    def _date_time_fields_utc(self):
        date_fields = super(FlightService, self)._date_time_fields_utc

        return [
            field for field in date_fields
            if field not in ('date_confirmed', )
        ]

    @property
    def _model_fields(self):
        return super(FlightService, self)._model_fields + [
            ('flight_status', FlightStatus)
        ]

    @property
    def _model_collection_fields(self):
        return super(FlightService, self)._model_collection_fields + [
            ('associated_services', AssociatedService),
        ]