from .tour import (  # NOQA
    Accommodation,
    Activity,
    OptionalActivity,
    Departure,
    DepartureComponent,
    Duration,
    Itinerary,
    ItineraryMedia,
    ItineraryHighlights,
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
    DossierFeature,
)

from .booking import (  # NOQA
    Agency,
    AgencyChain,
    Agent,
    Booking,
    Customer,
    Invoice,
    DeclinedReason,
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
    'Accommodation',
    'Activity',
    'Departure',
    'DepartureComponent',
    'Itinerary',
    'Promotion',
    'SingleSupplement',
    'Tour',
    'TourCategory',
    'TourDossier',
    'Transport',

    # Geographical
    'Airport',
    'Continent',
    'Country',
    'Feature',
    'FeatureCategory',
    'Place',
    'State',
    'Timezone',

    # Dossier
    'AccommodationDossier',
    'ActivityDossier',
    'DossierFeature',
    'PlaceDossier',
    'TransportDossier',
    'Language',
]

available_private_resources = [
    'AccommodationService',
    'ActivityService',
    'Agency',
    'AgencyChain',
    'Agent',
    'Booking',
    'Customer',
    'DeclinedReason',
    'DepartureService',
    'Document',
    'FeeService',
    'FlightService',
    'InsuranceService',
    'Invoice',
    'Nationality',
    'Payment',
    'Refund',
    'SingleSupplementService',
    'TransportService',
]

available_resources = available_public_resources + available_private_resources
