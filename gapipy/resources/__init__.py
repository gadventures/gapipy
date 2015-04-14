from .tour import (  # NOQA
    Accommodation,
    Activity,
    OptionalActivity,
    Departure,
    DepartureComponent,
    Duration,
    Itinerary,
    Promotion,
    SingleSupplement,
    Tour,
    TourCategory,
    TourDossier,
    Transport,
)

from .dossier import (  # NOQA
    AccommodationDossier,
    ActivityDossier,
    PlaceDossier,
    TransportDossier,
    DossierDetail,
    DossierDetailType,
)

from .booking import (  # NOQA
    Agency,
    Agent,
    Booking,
    Customer,
    Invoice,
    Document,
    Nationality,
    AccommodationService,
    ActivityService,
    DepartureService,
    FeeService,
    FlightService,
    InsuranceService,
    SingleSupplementService,
    TransportService,
    Payment,
    Refund,
)

from .geo import (  # NOQA
    Airport,
    Continent,
    Country,
    Feature,
    FeatureCategory,
    Place,
    State,
    Timezone,
)

from .language import Language  # NOQA


available_public_resources = [
    # Tour
    'Accommodation', 'Activity', 'Departure', 'Itinerary', 'Promotion',
    'SingleSupplement', 'Tour', 'TourCategory', 'TourDossier', 'Transport',
    'DepartureComponent',

    # Geographical
    'Airport', 'Continent', 'Country', 'Feature', 'FeatureCategory', 'Place',
    'State', 'Timezone',

    # Dossier
    'AccommodationDossier', 'ActivityDossier', 'PlaceDossier', 'TransportDossier',

    'Language',
]

available_private_resources = [
    'Agency', 'Agent', 'Booking', 'Customer', 'Invoice', 'Document',
    'Nationality', 'AccommodationService', 'ActivityService',
    'DepartureService', 'FeeService', 'FlightService', 'InsuranceService',
    'SingleSupplementService', 'TransportService', 'Payment', 'Refund',
]

available_resources = available_public_resources + available_private_resources
