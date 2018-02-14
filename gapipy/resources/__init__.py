from .tour import (  # NOQA
    Accommodation,
    Activity,
    OptionalActivity,
    Departure,
    DepartureComponent,
    Duration,
    Image,
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
    ServiceLevel,
    DossierSegment,
    CountryDossier,
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
    Override,
    OverrideReason,
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

from .checkin import (  # NOQA
    Checkin,
)

from .booking_company import BookingCompany
from .language import Language  # NOQA


available_public_resources = [
    # Tour
    'Accommodation',
    'Activity',
    'Departure',
    'DepartureComponent',
    'Image',
    'Itinerary',
    'Checkin',
    'Promotion',
    'SingleSupplement',
    'Tour',
    'TourCategory',
    'TourDossier',
    'Transport',
    'OverrideReason',

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
    'ServiceLevel',
    'DossierSegment',
    'CountryDossier',
]

available_private_resources = [
    'AccommodationService',
    'ActivityService',
    'Agency',
    'AgencyChain',
    'Agent',
    'Booking',
    'BookingCompany',
    'Checkin',
    'Customer',
    'DeclinedReason',
    'DepartureService',
    'Document',
    'FeeService',
    'FlightService',
    'InsuranceService',
    'Invoice',
    'Nationality',
    'Override',
    'Payment',
    'Refund',
    'SingleSupplementService',
    'TransportService',
]

available_resources = available_public_resources + available_private_resources
