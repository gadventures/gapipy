"""These tests mostly ensure that any change in the shape of the data
returned by the API is detected.
"""
import sys
from unittest import TestCase

from nose.plugins.attrib import attr
from nose_parameterized import parameterized

from gapipy.client import Client
from gapipy.resources import (
    Accommodation,
    AccommodationDossier,
    Activity,
    ActivityDossier,
    Airport,
    Checkin,
    Continent,
    Country,
    CountryDossier,
    Departure,
    DepartureComponent,
    DossierFeature,
    DossierSegment,
    Feature,
    FeatureCategory,
    Image,
    Itinerary,
    Language,
    Merchandise,
    OverrideReason,
    Place,
    PlaceDossier,
    Promotion,
    ServiceLevel,
    SingleSupplement,
    State,
    Timezone,
    Tour,
    TourCategory,
    TourDossier,
    Transport,
    TransportDossier,
    available_public_resources,
)


@attr('integration')
class TourTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tour = Client().tours.get(21715)

    def setUp(self):
        self.tour = TourTestCase.tour

    def test_get_itinerary(self):
        itin = self.tour.get_brief_itinerary()
        self.assertIsInstance(itin, list)


@attr('integration')
class TourDossierTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dossier = Client().tour_dossiers.get(24515)

    def setUp(self):
        self.dossier = TourDossierTestCase.dossier

    def test_get_itinerary(self):
        itin = self.dossier.get_detailed_itinerary()
        self.assertIsInstance(itin, list)

    def test_get_image_url(self):
        url = self.dossier.get_map_url()

        if sys.version_info.major < 3:
            # Python 2
            self.assertIsInstance(url, basestring)
        else:
            # Python 3
            self.assertIsInstance(url, str)

    def test_get_countries(self):
        countries = self.dossier.get_visited_countries()
        self.assertIsInstance(countries, list)

    def test_get_trip_detail(self):
        detail = self.dossier.get_trip_detail('Highlights')
        if sys.version_info.major < 3:
            # Python 2
            self.assertIsInstance(detail, basestring)
        else:
            # Python 3
            self.assertIsInstance(detail, str)

    def test_get_category_name(self):
        category = self.dossier.get_category_name('Trip Type')
        if sys.version_info.major < 3:
            # Python 2
            self.assertIsInstance(category, basestring)
        else:
            # Python 3
            self.assertIsInstance(category, str)


@attr('integration')
class LiveAPITestCase(TestCase):

    resources = [
        (Accommodation, 54),
        (AccommodationDossier, 5856),
        (Activity, 4486),
        (ActivityDossier, 9695),
        (Airport, 25553),
        (Checkin, 'q8YJAtaV9x'),
        (Continent, 'NA'),
        (Country, 'CA'),
        (CountryDossier, 10382),
        (Departure, 419504),
        (DepartureComponent, '55_3983802'),
        (DossierFeature, 4),
        (DossierSegment, 19),
        (Feature, 214),
        (FeatureCategory, 4),
        (Image, 4321),
        (Itinerary, 978),
        (Language, '250'),
        (Merchandise, 90867),
        (OverrideReason, 4),
        (Place, 2039527),
        (PlaceDossier, 711),
        (Promotion, 18336),
        (ServiceLevel, 3),
        (SingleSupplement, 'T419504'),
        (State, 'CA-ON'),
        (Timezone, 4),
        (Tour, 21715),
        (TourCategory, 15),
        (TourDossier, 24515),
        (Transport, 298),
        (TransportDossier, 51),
    ]

    def test_all_public_resources_are_tested(self):
        """This a bit meta, this is a test to ensure that all available
        (public) resources are included in this integration test case.
        """
        tested_resources = [r.__name__ for (r, pk) in self.resources]
        self.assertEqual(sorted(available_public_resources), sorted(tested_resources))

    @parameterized.expand(resources)
    def test_fetch_resource(self, resource, resource_id):

        # Test if a resource can be parsed properly. This is useful to catch
        # changes in the API
        api = Client()
        query = getattr(api, resource._resource_name)
        instance = query.get(resource_id)

        # Test that we take into account all of the fields of the json data
        # returned by the API (this only checks for the top-level fields, not
        # those of nested objects)
        self.assertEqual(
            sorted(instance._allowed_fields()),
            sorted(instance._raw_data.keys())
        )
