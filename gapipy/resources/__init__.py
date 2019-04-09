# flake8: NOQA
from .tour import (
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
    Merchandise,
    Promotion,
    SingleSupplement,
    Tour,
    TourCategory,
    TourDossier,
    Transport,
)

from .dossier import (
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

from .booking import (
    Agency,
    AgencyChain,
    Agent,
    Booking,
    Checkin,
    Customer,
    Invoice,
    DeclinedReason,
    Document,
    AccommodationService,
    ActivityService,
    DepartureService,
    FeeService,
    FlightService,
    InsuranceService,
    MerchandiseService,
    SingleSupplementService,
    TransportService,
    Payment,
    Refund,
    Requirement,
    RequirementSet,
    Override,
    OverrideReason,
)

from .geo import (
    Airport,
    Continent,
    Country,
    Feature,
    FeatureCategory,
    Nationality,
    Place,
    State,
    Timezone,
)

from .booking_company import BookingCompany
from .language import Language


available_public_resources = [
    # Tour
    'Accommodation',
    'Activity',
    'Departure',
    'DepartureComponent',
    'Image',
    'Itinerary',
    'Checkin',
    'Merchandise',
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
    'MerchandiseService',
    'Nationality',
    'Override',
    'Payment',
    'Refund',
    'Requirement',
    'RequirementSet',
    'SingleSupplementService',
    'TransportService',
]

available_resources = available_public_resources + available_private_resources
