.. :changelog:

History
=======

2.34.0 (2021-08-20)
-------------------

* Add ``travel_ready_policy`` model field to the ``Departure`` resource.
  * More details can be found in our `developer docs <https://developers.gadventures.com/docs/departure.html#travel-ready-policy>`


2.33.0 (2021-07-06)
-------------------

* Add ``online_preferences`` field to the ``Agency Chain`` resource.


2.32.0 (2021-06-18)
-------------------

* Make ``future`` requirement more flexible. See `PR #134`_ for more details.

.. _`PR #134`: https://github.com/gadventures/gapipy/pull/134


2.31.1 (2021-05-14)
-------------------

* Initialize the ``DjangoCache`` via the ``BaseCache`` which exposes the
  ``default_timeout`` attribute to the class. Prior to this change, when using
  the ``DjangoCache``, items would persist forever as no timeout would be set
  on the entries. See `PR #133`_ for more details.

.. note:: ``DjangoCache`` was introduced in `2.30.0 (2021-02-08)`_

.. _`PR #133`: https://github.com/gadventures/gapipy/pull/133


2.31.0 (2021-03-02)
-------------------

* Introduce ``gapipy.constants`` module that holds common constants. See
  `PR #132`_ for more details.

* Reintroduce the ability to enable old behaviour (pre `2.25.0 (2020-01-02)`_)
  for ``Resource.fetch``. It adds an optional ``httperrors_mapped_to_none``
  parameter to the method (default ``None``), where if a list of HTTP Status
  codes is provided instead, will silently consume errors mapped to those
  status codes and return a ``None`` value instead of raising the HTTPError.
  See `PR #131`_ for more details.

.. _`PR #131`: https://github.com/gadventures/gapipy/pull/131
.. _`PR #132`: https://github.com/gadventures/gapipy/pull/132


2.30.1 (2021-02-08)
-------------------

* Fix for `2.30.0 (2021-02-08)`_ Adds a guard against configuring Django
  settings again as per the `Django settings docs`_. See `PR #130`_ for more
  details.

.. _`Django settings docs`: https://docs.djangoproject.com/en/3.1/topics/settings/#either-configure-or-django-settings-module-is-required
.. _`PR #130`: https://github.com/gadventures/gapipy/pull/130


2.30.0 (2021-02-08)
-------------------

* Adds a new cache backend; ``gapipy.cache.DjangoCache``. It requires ``Django``
  and a ``gapi`` entry in ``settings.CACHES``. See `PR #129`_ for more details.

.. _`PR #129`: https://github.com/gadventures/gapipy/pull/129/

**Usage:**

* Set the ``GAPI_CACHE_BACKEND`` Env varible to ``gapipy.cache.DjangoCache``.

OR

.. code-block:: python

   from gapipy import Client

   gapi = Client(
      application_key="live_your-secret-gapi-key",
      cache_backend="gapipy.cache.DjangoCache",
   )


2.29.0 (2021-02-05)
-------------------

* Adds ``Departure.relationships`` field via ``DepartureRelationship`` model
* Adds ``TourDossier.relationships`` field via ``TourDossierRelationship``
  model

.. warning:: BREAKING!

* Moves the ``gapipy.resources.tour.itinerary.ValidDuringRange`` class over to
  its own file ``gapipy.models.valid_duraing_range.ValidDuringRange``
  so that it can be reused by the ``TourDossierRelationship`` model. Any code
  importing the class directly will need to change the import path:

   .. code-block:: python

      # before
      from gapipy.resources.tour.itinerary.ValidDuringRange

      # now
      from gapipy.models import ValidDuringRange

* See `PR #128`_ for more details.

.. _`PR #128`: https://github.com/gadventures/gapipy/pull/128/


2.28.0 (2020-11-23)
-------------------

* Add a new ``Client`` config option, ``global_http_headers``, a dict of HTTP
  headers to add to each request made with that client.

  This is similar to the ``headers=`` kwargs available when making ``get`` and
  ``create`` calls, except that the ``global_http_headers`` set on a client
  will apply on *every request* made by that client instance.


2.27.0 (2020-05-26)
-------------------

.. warning:: BREAKING!

* Make ``Customer.nationality`` a *resource field*. This allows attribute style
  access to the field values, whereas before they needed to be accessed using
  dictionary accessor (``d["key"]``) syntax.

.. code-block:: python

   # before
   >>> api.customers.get(123456).nationality["name"]
   u'Canadian'

   # now
   >>> api.customers.get(123456).nationality.name
   u'Canadian'


2.26.4 (2020-04-28)
-------------------

* Fix `2.26.3 (2020-04-28) (Yanked)`_: Add missing ``CONTRIBUTING.rst`` to the
  manifest.

.. note:: Discovered when attempting to install ``gapipy`` via ``pip``.


2.26.3 (2020-04-28) (Yanked)
----------------------------

* Fix py2 & py3 compatibility for ``urlparse``


2.26.2 (2020-04-20)
-------------------

* Fix for `2.26.1 (2020-04-20)`_ and `Issue #113`_.

   * See `PR #125`_.
   * Remove the ``_set_resource_collection_field`` method in ``TourDossier``
   * Introducing the ``_Parent`` namedtuple in `PR #123`_.
     broke being able to Query-chain from Tour-Dossiers to departures
   * Buggy behaviour fixed from `2.26.1 (2020-04-20)`_

   .. code-block:: python

      >>> from gapipy import Client
      >>> api = Client(application_key='MY_SECRET_KEY')

      >>> api.tour_dossiers(24309).departures.count()
      # AttributeError: 'tuple' object has no attribute 'uri'

.. _`PR #125`: https://github.com/gadventures/gapipy/pull/125


2.26.1 (2020-04-20)
-------------------

* Fix for `2.26.0 (2020-04-14)`_ and `Issue #113`_.

   * Calls to ``APIRequestor.list_raw`` will use initialised its parameters,
     unless the URI provides its own.
   * See `PR #123`_.

* Add the ability to define the ``max_retries`` values on the requestor.

   * New ``env`` value ``GAPI_CLIENT_MAX_RETRIES``.
   * The default value will be ``0``, and if provided will override the ``retry``
     value on the ``requests.Session``.
   * This change will also always initialize a ``requests.Session`` value on
     initialisation of the ``gapipy.Client``.
   * See `PR #124`_.

* Add ``variation_id`` field to the ``Image`` resource.

   * See `Commit edc8d9b`_.

* Update the ``ActivityDossier`` and ``AccommodationDossier`` resources.

   * Remove the ``is_prepaid`` field.
   * Adds the ``has_costs`` field.
   * See `Commit bd35531`_. 

.. _`Issue #113`: https://github.com/gadventures/gapipy/issues/113
.. _`PR #123`: https://github.com/gadventures/gapipy/pull/123
.. _`PR #124`: https://github.com/gadventures/gapipy/pull/124
.. _`Commit edc8d9b`: https://github.com/gadventures/gapipy/commit/edc8d9b
.. _`Commit bd35531`: https://github.com/gadventures/gapipy/commit/bd35531


2.26.0 (2020-04-14)
-------------------

.. warning:: BREAKING!

* The ``Query.filter`` method will return a clone/copy of itself. This will
  preserve the state of ``filters`` on the original Query object.
* The ``Query.all`` method will **not** clear the filters after returning.
* The ``Query.all`` method will return a ``TypeError`` if a type other than
  an ``int`` is passed to the ``limit`` argument.
* The ``Query.count`` method will **not** clear the filters after returning.
* See `PR #121`_ for more details.

New behaviour with the ``Query.filter`` method:

.. code-block:: python

   >>> from gapipy import Client
   >>> api = Client(application_key='MY_SECRET_KEY')

   # create a filter on the departures
   >>> query = api.departures.filter(**{"tour_dossier.id": "24309"})
   >>> query.count()
   494

   # we preserve the filter status of the current query
   >>> query.filter(**{"availability.status": "AVAILABLE"}).count()
   80

   >>> query.count()
   494

* The ``AgencyChain.agencies`` attribute returns a list of ``Agency`` objects.
  See `Commit f34afd52`_.

.. _`PR #121`: https://github.com/gadventures/gapipy/pull/121
.. _`Commit f34afd52`: https://github.com/gadventures/gapipy/commit/f34afd52


2.25.1 (2020-01-02)
-------------------

* Improve contribution instructions to check long_description rST file in dist
* Dev Requirement updates:

   * Add ``readme_renderer==24.0``
   * Add ``twine==1.15.0`` for ``twine check`` command


2.25.0 (2020-01-02)
-------------------

* Failing to fetch inlined Resource (from Stubs) will raise the underlying
  requests.HTTPError instead of AttributeError resulting from a ``None``.
* Adds ``httperrors_mapped_to_none`` kwarg to ``gapipy.query.Query.get``
  with default value ``gapipy.query.HTTPERRORS_MAPPED_TO_NONE``
* Modifies ``gapipy.resources.base.Resource.fetch`` to
  pass ``httperrors_mapped_to_none=None`` to ``Query.get``
* This ensures that any underlying ``requests.HTTPError`` from ``Query.get``
  is bubbled up to the caller. It is most prevalent when reference Resource stubs
  fail to be retrieved from the G API. Prior to this change ``Resource.fetch``
  would return a ``None`` value resulting in an ``AttributeError``. Now, if the
  stub fails to fetch due to an HTTPError, that will be raised instead


2.24.3 (2019-12-12)
-------------------

* Exclude the ``tests`` package from the package distribution


2.24.2 (2019-12-12)
-------------------

* Adds the ``compute_request_signature`` and ``compute_webhook_validation_key``
  utility methods. See `PR #122`_.

.. _`PR #122`: https://github.com/gadventures/gapipy/pull/122


2.24.1 (2019-12-12)
-------------------

* Add ``slug`` field to ``TourDossier`` resource. See `PR #120`_.

.. _`PR #120`: https://github.com/gadventures/gapipy/pull/120


2.24.0 (2019-11-05)
-------------------

* Add missing/new fields to the following resources. See `PR #117`_.

   * AccommodationDossier: ``categories``, ``suggested_dossiers``, ``visited_countries``, ``visited_cities``
   * ActivityDossier: ``suggested_dossiers``, ``visited_countries``, ``visited_cities``
   * Departure: ``local_payments``
   * Itinerary: ``publish_state``

* Add ``continent`` and ``place`` references to the ``Countries`` resource. See
  `PR #115`_.
* Accept ``additional_headers`` optional kwarg on ``create``. See `PR #114`_.

.. _`PR #114`: https://github.com/gadventures/gapipy/pull/114
.. _`PR #115`: https://github.com/gadventures/gapipy/pull/115
.. _`PR #117`: https://github.com/gadventures/gapipy/pull/117


2.23.0 (2019-11-04)
-------------------

* Remove deprecated ``tour_dossiers.itineraries`` field and related code


2.22.0 (2019-10-10)
-------------------

* Add ``booking_company`` field to ``Booking`` resource


2.21.0 (2019-04-09)
-------------------

* Add ``ripple_score`` to ``Itinerary`` resource


2.20.1 (2019-02-20)
-------------------

* HISTORY.rst doc fixes


2.20.0 (2019-02-20)
-------------------

* Add ``Requirement`` and ``RequirementSet`` resources
* Move ``Checkin`` resource to the ``resources.booking`` module
* The ``Query`` object will resolve to use the ``href`` value when
  returning the iterator to fetch ``all`` of some resource. This is
  needed because ``bookings/123456/requirements`` actually returns a list
  of ``RequirementSet`` resources
* See `Release tag 2.20.0`_ for more details.

.. _`Release tag 2.20.0`: https://github.com/gadventures/gapipy/releases/tag/2.20.0


2.19.4 (2019-02-14)
-------------------

* Add ``get_category_name`` helper method to ``TourDossier`` resource


2.19.3 (2019-02-12)
-------------------

* Attempt to fix rST formatting of ``README`` and ``HISTORY`` on pypi


2.19.2 (2019-02-12)
-------------------

* Become agnostic between redis ``2.x.x`` && ``3.x.x`` versions

   * the ``setex`` method argument order changes between the major versions


2.19.1 (2019-02-12)
-------------------

.. note:: HotFix for `2.19.0 (2019-02-12)`_.

* adds ``requirements.txt`` file to the distribution ``MANIFEST``


2.19.0 (2019-02-12)
-------------------

* Add ``booking_companies`` field to ``Itinerary`` resource
* Pin our requirement/dependency versions

   * pin ``future == 0.16.0``
   * pin ``requests >= 2.18.4, < 3.0.0``
   * read ``setup.py`` requirements from ``requirements.txt``


2.18.1 (2019-02-07)
-------------------

* Add ``customers`` nested resource to ``bookings``


2.18.0 (2018-12-14)
-------------------

* Add ``merchandise`` resource
* Add ``merchandise_services`` resources


2.17.0 (2018-11-12)
-------------------

* Add ``membership_programs`` field to the ``Customer`` resource


2.16.0 (2018-11-07)
-------------------

* Completely remove the deprecated ``add_ons`` field from the Departure resource
* Add missing fields to various Dossier resources

   * AccommodationDossier: ``flags``, ``is_prepaid``, ``service_time``, ``show_on_reservation_sheet``
   * ActivityDossier: ``is_prepaid``, ``service_time``, ``show_on_reservation_sheet``
   * CountryDossier: ``flags``
   * PlaceDossier: ``flags``
   * TransportDossier: ``flags``

* Add ``valid_during_ranges`` list field to the Itinerary resource. This field is
  a list field of the newly added ``ValidDuringRange`` model (described below)
* Add ``ValidDuringRange`` model. It consists of two date fields, ``start_date``,
  and ``end_date``. It also provides a number of convenience methods to determine
  if the date range provided is valid, or relative to some date.

   * ``is_expired``: Is it expired relative to ``datetime.date.today``
   * ``is_valid_today``: Is it valid relative to ``datetime.date.today``
   * ``is_valid_during_range``: Is it valid for some give start/end date range
   * ``is_valid_on_or_after_date``: Is it valid on or after some date
   * ``is_valid_on_or_before_date``: Is it valid on or before some date
   * ``is_valid_on_date``: Is it valid on some date
   * ``is_valid_sometime``: Is it valid at all


2.15.0 (2018-10-10)
-------------------

* Add ``country`` reference to ``Nationality`` resource.
* Moved ``resources/bookings/nationality.py`` to ``resources/geo/*``.


2.14.6 (2018-08-01)
-------------------

* Check for presence of ``id`` field directly in the Resource ``__dict__`` in
  order to prevent a chicken/egg situation when attempting to ``save``. This is
  needed due to the change introduced in 2.14.4, where we explicitly raise an
  AttributeError when trying to access the ``id`` attribute.
* Added ``service_code`` field for Activty & Accommodation Dossier resources.


2.14.5 (2018-08-01)
-------------------

* deleted


2.14.4 (2018-07-13)
-------------------

* Raise an ``AttributeError`` when trying to access ``id`` on
  ``Resource.__getattr__``.
* Don't send duplicate params when paginating through list results.
* Implement ``first()`` method for ``Query``.

2.14.3 (2018-05-29)
-------------------

* Expose Linked Bookings via the API.

2.14.1 (2018-05-15)
-------------------

* Add ``booking_companies`` field to Agency resource.
* Remove ``bookings`` field from Agency resource.
* Add ``requirements`` as_is field to Departure Service resource.
* Add ``policy_emergency_phone_number`` field to Insurance Service resource.


2.14.0 (2018-05-15)
-------------------

* Remove deprecated ``add_ons`` field from ``Departure`` resource.
* Add ``costs`` field to ``Accommodation`` & ``ActivityDossier`` resources.


2.13.0 (2018-03-31)
-------------------

* Add ``meal_budgets`` list field to ``CountryDossier`` resource.
* Add ``publish_state`` field to ``DossierFeatures`` resource.


2.12.0 (2018-02-14)
-------------------

* Add optional ``headers`` parameter to Query.get to allow HTTP-Headers to be
  passed. e.g. ``client.<resource>.get(1234, headers={'A':'a'})``. See
  `PR #91`_.
* Add ``preferred_display_name`` field to ``Agency`` resource. See `PR #92`_.
* Add ``booking_companies`` array field to all Product-type resources. See
  `PR #93`_.

   * Accommodation
   * Activity
   * AgencyChain
   * Departure
   * SingleSupplement
   * TourDossier
   * Transport

.. _`PR #91`: https://github.com/gadventures/gapipy/pull/91
.. _`PR #92`: https://github.com/gadventures/gapipy/pull/92
.. _`PR #93`: https://github.com/gadventures/gapipy/pull/93


2.11.4 (2018-01-29)
-------------------

* Add ``agency_chain`` field to ``Booking`` resource
* Add ``id`` field as part of the ``DossierDetail`` model See `PR #89`_.
* Add ``agency_chains`` field to the ``Agency`` resource. See `PR #90`_.
* See `Release tag 2.11.3`_ for more details.

.. _`PR #89`: https://github.com/gadventures/gapipy/pull/89
.. _`PR #90`: https://github.com/gadventures/gapipy/pull/90
.. _`Release tag 2.11.3`: https://github.com/gadventures/gapipy/releases/tag/2.11.3


2.11.0 (2017-12-18)
-------------------

* The ``Customer.address`` field uses the ``Address`` model, and is no longer a
  dict.
* Passing in ``uuid=True`` to ``Client`` kwargs enables ``uuid`` generation
  for every request.


2.10.0 (2017-12-01)
-------------------

* Add the ``amount_pending`` field to the ``Booking`` resource
* The ``PricePromotion`` model extends from the ``Promotion`` resource (PR/85)
* Update the ``Agent`` class to use BaseModel classes for the ``role``
  and ``phone_numbers`` fields.
* see `Release tag 2.10.0`_ for more details.

.. _`Release tag 2.10.0`: https://github.com/gadventures/gapipy/releases/tag/2.10.0


2.9.3 (2017-11-23)
------------------

.. note:: We have skipped Release ``2.9.2`` due to pypi upload issues.

* Expose ``requirement_set`` for ``departure_services`` & ``activity_services``.


2.9.1 (2017-11-22)
------------------

.. note:: * We have skipped Release ``2.9.0`` due to pypi upload issues.

* Adds the ``options`` method on the Resource Query object. See
  `Release tag 2.9.1`_ for more details.

.. _`Release tag 2.9.1`: https://github.com/gadventures/gapipy/releases/tag/2.9.1


2.8.2 (2017-11-14)
------------------

* Adds fields ``sale_start_datetime`` and ``sale_finish_datetime`` to the
  Promotion resource. The fields mark the start/finish date-time values
  for when a Promotion is applicable. The values represented are in UTC.


2.8.1 (2017-10-25)
------------------

* Add new fields to the ``Agency`` and ``AgencyChain`` resources


2.8.0 (2017-10-23)
------------------

* This release adds a behaviour change to the ``.all()`` method on resource
  Query objects. Prior to this release, the base Resource Query object would
  retain any previously added ``filter`` values, and be used in subsequent
  calls. Now the underlying filters are reset after a ``<resource>.all()`` call
  is made.

  See `Issue #76`_ and `PR #77`_ for details and the resulting fix. 

* Adds missing fields to the Agency and Flight Service resources (PR/78)

.. _`Issue #76`: https://github.com/gadventures/gapipy/issues/76
.. _`PR #77`: https://github.com/gadventures/gapipy/pull/77


2.7.6 (2017-10-04)
------------------

* Add ``agency`` field to ``Booking`` resource.


2.7.5 (2017-09-25)
------------------

* Add test fix for Accommodation. It is a listable resource as of ``2.7.4``
* Add regression test for departures.addon.product model
  * Ensure Addon's are instantiated to the correct underlying model.
  * Prior to this release, all Addon.product resources were instantiated as
  ``Accommodation``.


2.7.4 (2017-09-20)
------------------

* Add ``videos``, ``images``, and ``categories`` to ``Activity``, ``Transport``,
  ``Place``, and ``Accommodation Dossier`` resources.
* Add ``flags`` to Itinerary resource
* Add list view of ``Accommodations`` resource


2.7.3 (2017-09-06)
------------------

* Add ``type`` field to ``AgencyDocument`` model
* Add ``structured_itinerary`` model collection field to ``Departure`` resource


2.7.2 (2017-08-18)
------------------

* Fix flight_status Reference value in FlightService resource


2.7.1 (2017-08-18)
------------------

* Fix: remove FlightStatus import reference for FlightService resource
* Add fields (fixes two broken Resource tests)

  * Add ``href`` field for ``checkins`` resource
  * Add ``date_cancelled`` field for ``departures`` resource

* Fix broken ``UpdateCreateResource`` tests


2.7.0 (2017-08-18)
------------------

* Remove ``flight_statuses`` and ``flight_segments`` resources.


2.6.2 (2017-08-11)
------------------

* Version bump


2.6.1 (2017-08-11)
------------------

* Adds a Deprecation warning when using the ``tours`` resource.


2.6.0 (2017-08-11)
------------------

* Fixed `Issue #65`_: only
  write data into the local cache after a fetch from the API, do not write data
  into the local cache when fetching from the local cache.

.. _`Issue #65`: https://github.com/gadventures/gapipy/issues/65


2.5.2 (2017-04-26)
------------------

* Added ``future`` dependency to setup.py


2.5.1 (2017-02-08)
------------------

* Fixed an issue in which modifying a nested dictionary caused gapipy to not
  identify a change in the data.
* Added ``tox.ini`` for testing across Python platforms.
* Capture ``403`` Status Codes as a ``None`` object.

2.5.0 (2017-01-20)
------------------

* Provided Python 3 functionality (still Python 2 compatible)
* Removed Python 2 only tests
* Installed ``future`` module for smooth Python 2 to Python 3 migration
* Remove ``DictToModel`` class and the associated tests
* Add ``Dossier`` Resource(s)
* Minor field updates to: ``Customer``, ``InsuranceService``,
  ``DepartureService``, ``Booking``, ``FlightStatus``, ``State``


2.4.9 (2016-11-22)
------------------

* Fixed a bug with internal ``_get_uri`` function.


2.4.8 (2016-11-11)
------------------

* Adjusted ``Checkin`` resource to meet updated spec.


2.4.7 (2016-10-25)
------------------

* Added ``Checkin`` resource.


2.4.6 (2016-10-19)
------------------

* Fix broken ``Duration`` init in ``ActivityDossier`` (likely broke due to
  changes that happened in 2.0.0)


2.4.5 (2016-10-13)
------------------

* Added ``Image`` resource definition and put it to use in ``Itinerary`` and,
  ``PlaceDossier``


2.4.4 (2016-09-09)
------------------

* Added ``date_last_modified`` and ``date_created`` to ``Promotion``.


2.4.3 (2016-09-06)
------------------

* Added ``gender`` to ``Customer``.
* Added ``places_of_interest`` to ``Place``.


2.4.2 (2016-07-08)
------------------

* Added ``departure`` reference to ``DepartureComponent``


2.4.1 (2016-07-06)
------------------

* Removed use of ``.iteritems`` wherever present in favour of ``.items``
* Added ``features`` representation to ``ActivityDossier`` and,
  ``TransportDossier``


2.4.0 (2016-06-29)
------------------

* Added ``CountryDossier`` resource.


2.3.0 (2016-06-28)
------------------

* Added ``DossierSegment`` resource.
* Added ``ServiceLevel`` resource.


2.2.2 (2016-06-08)
------------------

* Added day ``label`` field to the ``Itinerary`` resource.


2.2.1 (2016-06-06)
------------------

* Added ``audience`` field to the ``Document`` resource.


2.2.0 (2016-05-17)
------------------

* Added ``transactional_email``, and ``emails`` to ``Agency`` resource.


2.1.2 (2016-05-17)
------------------

* Added ``audience`` to ``Invoice`` resource.


2.1.1 (2016-04-29)
------------------

* Removed invalid field, ``email`` from ``AgencyChain``


2.1.0 (2016-04-25)
------------------

* Added new resource, ``AgencyChain``


2.0.0 (2016-03-11)
------------------

The global reference to the last instantiated ``Client`` has been removed. It
is now mandatory to pass in a Client instance when instantiating a ``Model`` or
``Resource``.

In practice, this should not introduce too many changes in codebases that are
using ``gapipy``, since most resource interacation happens through a ``Client``
instance (e.g. ``api.tours.get(123)``, or ``api.customers.create({...})``),
instead of being instantiated independently. The one possible exception is unit
testing: in that case, ``Client.build`` can be useful.

The global variable was causing issues with connection pooling when multiple
client with different configurations were used at the same time.


1.1.0 (2016-03-11)
------------------

* Added new resource, ``DossierFeature``


1.0.0 (2016-02-29)
------------------

* Adopted `Semantic Versioning`_ for this project.

.. warning:: BREAKING!

* Refactored how the cache key is set. This is a breaking change for any
  modules that implemented their own cache interface. The cache modules are
  no longer responsible for defining the cache value, but simply storing
  whatever it is given into cache. The ``Query`` object now introduces a
  ``query_key`` method which generates the cache key sent to the cache
  modules.

.. _`Semantic Versioning`: http://semver.org/


0.6.3 (2016-01-21)
------------------

* Added better error handling to ``Client.build``. An AttributeError raised when
  instantiating a resource won't be shadowed by the except block anymore.


0.6.2 (2016-01-20)
------------------

* Fixed a regression bug when initializing DepartureServiceRoom model.


0.6.1 (2016-01-20)
------------------

* Fixed a regression bug when initializing services.


0.6.0 (2016-01-20)
------------------

* Fixed a bug when initializing list of resources.


0.5.5 (2016-01-08)
------------------

* Added a component of type ``ACCOMMODATION`` to ``Itineraries``.


0.5.4 (2016-01-04)
------------------

* Added ``associated_services`` to ``SingleSupplementService``


0.5.3 (2015-12-31)
------------------

* Added ``name`` to ``Departure``.
* Happy New Year!


0.5.2 (2015-12-15)
------------------

* Added ``variation_id`` to ``BaseCache`` to fix a ``TypeError`` when using
  the ``NullCache``


0.5.1 (2015-12-14)
------------------

* Add ``associated_agency`` to ``bookings`` resource


0.5.0 (2015-12-10)
------------------

* Minor adjusted in Query internals to ensure the ``variation_id`` of an
  Itinerary is handled properly.
* Added ``ItineraryHighlights`` and ``ItineraryMedia`` resources. These are
  sub resources of the ``Itinerary``


0.4.6 (2015-12-09)
------------------

* Added connection pool caching to ``RedisCache``. Instances of ``gapipy`` with
  the same cache settings (in the same Python process) will share a connection
  pool.


0.4.5 (2015-11-05)
------------------

* Added ``code`` field to the ``type`` of an ``Itinerary``'s listed
  ``details``.


0.4.4 (2015-11-04)
------------------

* Added the ``details`` field to the ``Itinerary`` resource -- a list of
  textual details about an itinerary.


0.4.3 (2015-11-03)
-------------------

* Added the ``tour_dossier`` field to the ``Itinerary`` resource.


0.4.2 (2015-10-28)
------------------

* Fixed a bug that would cause ``amount`` when looking at ``Promotion`` objects
  in the ``Departure`` to be removed from the data dict.


0.4.1 (2015-10-16)
------------------

* Moved an import of ``requests`` down from the module level. Fixes issues in
  CI environments.


0.4.0 (2015-10-13)
------------------

* Added connection pooling options, see docs for details on
  ``connection_pool_options``.


0.3.0 (2015-09-24)
------------------

* Modified how the ``Promotion`` object is loaded within ``price_bands`` on a
  ``Departure``. It now correctly captures the ``amount`` field.


0.2.0 (2015-09-15)
------------------

* Modified objects within ``cache`` module to handle ``variation_id``, which is
  exposed within the ``Itinerary`` object. Previously, the ``Itinerary`` would
  not be correctly stored in cache with its variant reference.


0.1.51 (2015-08-31)
-------------------

* Added the ``components`` field to the ``Departure`` resource.


0.1.50 (2015-07-28)
-------------------

* Fixed an issue with the default ``gapipy.cache.NullCache`` when ``is_cached``
  was used.


0.1.49 (2015-07-23)
-------------------

* Added new fields to ``Itinerary`` revolving around variations.
* Added ``declined_reason`` to all service resources.


0.1.48 (2015-07-15)
-------------------

* Add DeclinedReason resource


0.1.47 (2015-07-08)
-------------------

* Fixed a bug in ``APIRequestor.get``. Requesting a resource with with an id of
  ``0`` won't raise an Exception anymore.


0.1.46 (2015-06-10)
-------------------

* Added ``associated_services`` and ``original_departure_service`` to various
  service resources and ``departure_services`` model respectively.


0.1.45 (2015-05-27)
-------------------

* Fixed ``products`` within the ``Promotion`` resource to properly retain
  ``type`` and ``sub_type`` fields after being parsed into a dictionary.


0.1.44 (2015-05-22)
-------------------

* Changed default ``cache_backend`` to use ``gapipy.cache.NullCache``.
  Previously, ``SimpleCache`` was the default and led to confusion in
  production environments, specifically as to why resources were not matching
  the API output. Now, by default, to get any caching from gapipy you must
  explicitly set it.


0.1.43 (2015-04-29)
-------------------

* Fixed ``Place`` init with empty admin_divisions.


0.1.42 (2015-04-29)
-------------------

* Added ``description`` to ``TourCategory`` resource.


0.1.41 (2015-04-14)
-------------------

* Added ``DepartureComponent`` resource. See the official G API
  `documentation <https://developers.gadventures.com/docs/departure_component.html>`_
  for details.


0.1.40 (2015-04-06)
-------------------

* Added ``deposit`` to ``DepartureService`` resource.


0.1.39 (2015-03-31)
-------------------

* Refactor ``APIRequestor._request``. While this should not change existing
  functionality, it is now possible to override specific methods on the class.


0.1.38 (2015-03-23)
-------------------

* Fixed: Due to inconsistencies in the G API with regards to nested resources,
  the ``fetch`` function was modified to use the raw data from the API, rather
  than a specific set of allowed fields.


0.1.37 (2015-03-23)
-------------------

* Fixed: Iterating over ``products`` within the ``promotions`` object now works
  as expected. Previously, accessing the ``products`` attribute would result in
  a Query object with incorrect parameters.


0.1.36 (2015-03-17)
-------------------

* Support free to amount price range formatting (e.g. Free-10CAD)


0.1.35 (2015-03-12)
-------------------

* Added ``duration_min`` & ``duration_max`` to ``ActivityDossier`` model


0.1.34 (2015-03-11)
-------------------

* Added ``OptionalActivity`` model
* All Dossiers with ``details``:
  * Now represented as list of ``DossierDetail`` models
  * Added convenience methods for retrieving specific details
* ``ItineraryComponent`` and ``ActivityDossier`` use new ``Duration`` model
  for their ``duration`` field/property
* Added ``duration_label`` and ``location_label`` to ``ItineraryComponent``
* Added ``duration_label``, ``price_per_person_label``, and
  ``price_per_group_label`` to ``ActivityDossier``


0.1.33 (2015-03-02)
-------------------

* Added ``name`` field to the Itinerary resource.


0.1.32 (2015-02-18)
-------------------

* Changed cache key creation to account for ``GAPI_LANGUAGE`` when the
  environment variable is set.


0.1.31 (2015-02-18)
-------------------

* Fixed a bug when setting _resource_fields in ``DepartureService`` resource


0.1.30 (2015-02-11)
-------------------

* ``TourDossier.structured_itineraries`` now refers to a list of Itinerary
  resources


0.1.29 (2015-02-10)
-------------------

* Added ``TransportDossier`` and ``Itinerary`` resources.

* The reference to the itinerary in a ``DepartureService`` is now a
  full-fledged ``Itinerary`` resource.


0.1.28 (2015-01-22)
-------------------

* Bug fix to correctly send ``Content-Type: application/json`` in POST, PUT,
  or PATCH.


0.1.27 (2015-01-19)
-------------------

* Update ``DepartureService`` object to contain a reference to its
  ``Itinerary``


0.1.26 (2015-01-14)
-------------------

* Normalize API request headers, to promote caching.


0.1.25 (2015-01-09)
-------------------

* Added ``ActivityDossier`` and ``AccommodationDossier`` resources, as well as
  references to it from ``Activity`` and ``Accommodation``.


0.1.24 (2015-01-07)
-------------------

* Added ``PlaceDossier`` resource, as well as reference to it from ``Place``


0.1.22 (2014-12-12)
-------------------

* Added ``advertised_departures`` to ``TourDossier``


0.1.21 (2014-11-26)
-------------------

* Fixed a bug with promotions on a Price object. When promotions were accessed,
  gapipy would query for all promotions, rather than returning the inline list.


0.1.20 (2014-11-20)
-------------------

* Departure resource is now listable via filters.


0.1.19 (2014-11-17)
-------------------

* Fixed a bug with ``RedisCache`.is_cached` where it would not use the set
  ``key_prefix`` when checking for existence in cache. Effectively, it would
  always return False


0.1.18 (2014-11-12)
-------------------

* When setting a ``date_field``, initiate it as a ``datetime.date`` type.


0.1.17 (2014-11-07)
-------------------

* Deprecated ``RedisHashCache`` from cache backends available by default. Was not
  well tested or reliable.


0.1.16 (2014-10-28)
---------------------

* Fixed a bug where if a model field received ``null`` as a value, it would fail.
  Now, if the result is ``null``, the model field will have an appropriate ``None``
  value.


0.1.15 (2014-10-23)
-------------------

* Fix a bug in the DepartureRoom model. The ``price_bands`` attribute is now
  properly set.


0.1.14 (2014-10-22)
-------------------

* Fixed a bug where AgencyDocument was not included in the code base.


0.1.13 (2014-10-21)
-------------------

* Add ``latitude``, ``longitude``, and ``documents`` to the ``Agency``
  resource.


0.1.12 (2014-10-20)
-------------------

* ``date_created`` on the ``Agency`` resource is correctly parsed as a local
  time.


0.1.11 (2014-10-15)
-------------------

* Improve the performance of ``Resource.fetch`` by handling cache get/set.


0.1.10 (2014-10-09)
-------------------

* Fix a bug in AccommodationRoom price bands. The ``season_dates`` and
  ``blackout_dates`` attributes are now properly set.


0.1.9 (2014-09-23)
------------------

* Add `iso_639_3` and `iso_639_1` to ``Language``


0.1.8 (2014-09-17)
------------------

* Remove the ``add_ons`` field in ``Departure``, and add ``addons``.


0.1.7 (2014-08-22)
------------------

* Fix a bug when initializing AccommodationRoom from cached data.


0.1.6 (2014-08-19)
------------------

* Add Query.purge_cached


0.1.5 (2014-07-29)
------------------

* Add ``details`` field to the list of ``incomplete_requirements`` in a
  ``DepartureService``.


0.1.4 (2014-07-21)
------------------

* Removed sending of header `X-HTTP-Method-Override: PATCH` when the update
  command is called. Now, when `.save(partial=True)` is called, the
  correct PATCH HTTP method will be sent with the request.


0.1.3 (2014-07-18)
------------------

* Return ``None`` instead of raising a HTTPError 404 exception when fetching a
  non-existing resource by id.
* Added ability to create resources from the Query objects on the client
  instance.

.. code-block:: python

   obj = {'name': {'legal_first_name': 'Pat', ...}, ...}
   api.customers.create(obj)


0.1.2 (2014-07-14)
------------------

* Added Query.is_cached
* Added cache options


0.1.1 (2014-06-27)
------------------

* Use setuptools find_packages


0.1.0 (2014-06-20)
------------------

* First release on PyPI.
