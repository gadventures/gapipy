.. :changelog:

History
=======

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

The global reference to the last instantiated Client has been removed. It is
now mandatory to pass in a Client instance when instantiating a Model or
Resource.

In practice, this should not introduce too much changes in codebases that are
using ``gapipy``, since resources are mostly interacted with through a Client
instance (for example, ``api.tours.get(123)``, or
``api.customers.create({...})``), instead of being instantiated independently.
The one possible exception is unit testing: in that case, ``Client.build`` can
be useful.

The global variable was causing issues with connection pooling when multiple
client with different configurations were used at the same time.

1.1.0 (2016-03-11)
------------------

* Added new resource, ``DossierFeature``

1.0.0 (2016-02-29)
------------------

* Adopted `Semantic Versioning <http://semver.org/>`_ for this project.
* Refactored how the cache key is set. This is a breaking change for any modules that implemented their own cache interface. The cache modules are no longer responsible for defining the cache value, but simply storing whatever it is given into cache. The ``Query`` object now introduces a ``query_key`` function which generates the cache key sent to the cache modules.

0.6.3 (2016-01-21)
------------------

* Added better error handling to `Client.build`. An AttributeError raised when instantiating a resource won't be shadowed by the except block anymore.


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

* Added ``variation_id`` to ``BaseCache`` to fix a ``TypeError`` when using the ``NullCache``

0.5.1 (2015-12-14)
------------------

* Add ``associated_agency`` to ``bookings`` resource

0.5.0 (2015-12-10)
------------------

* Minor adjusted in Query internals to ensure the ``variation_id`` of an Itinerary is handled properly.
* Added ``ItineraryHighlights`` and ``ItineraryMedia`` resources. These are sub resources of the ``Itinerary``

0.4.6 (2015-12-09)
------------------

* Added connection pool caching to ``RedisCache``. Instances of ``gapipy`` with the same cache settings (in the same Python process) will share a connection pool.

0.4.5 (2015-11-05)
------------------

* Added ``code`` field to the ``type`` of an ``Itinerary``'s listed ``details``.

0.4.4 (2015-11-04)
------------------

* Added the ``details`` field to the ``Itinerary`` resource -- a list of textual details about an itinerary.

0.4.3 (2015-11-03)
-------------------

* Added the ``tour_dossier`` field to the ``Itinerary`` resource.

0.4.2 (2015-10-28)
------------------

* Fixed a bug that would cause ``amount`` when looking at ``Promotion`` objects in the ``Departure`` to be removed from the data dict.

0.4.1 (2015-10-16)
------------------

* Moved an import of ``requests`` down from the module level. Fixes issues in CI environments.

0.4.0 (2015-10-13)
------------------

* Added connection pooling options, see docs for details on ``connection_pool_options``.

0.3.0 (2015-09-24)
------------------

* Modified how the ``Promotion`` object is loaded within ``price_bands`` on a ``Departure``. It now correctly captures the ``amount`` field.

0.2.0 (2015-09-15)
------------------

* Modified objects within ``cache`` module to handle ``variation_id``, which is exposed within the ``Itinerary`` object. Previously, the ``Itinerary`` would not be correctly stored in cache with its variant reference.

0.1.51 (2015-08-31)
-------------------

* Added the ``components`` field to the ``Departure`` resource.


0.1.50 (2015-07-28)
-------------------

* Fixed an issue with the default ``gapipy.cache.NullCache`` when ``is_cached`` was used.

0.1.49 (2015-07-23)
-------------------

* Added new fields to ``Itinerary`` revolving around variations.
* Added ``declined_reason`` to all service resources.

0.1.48 (2015-07-15)
-------------------

* Add DeclinedReason resource

0.1.47 (2015-07-08)
-------------------

* Fixed a bug in ``APIRequestor.get``. Requesting a resource with with an id of ``0`` won't raise an Exception anymore.

0.1.46 (2015-06-10)
-------------------

* Added ``associated_services`` and ``original_departure_service`` to various service resources and ``departure_services`` model respectively.

0.1.45 (2015-05-27)
-------------------

* Fixed ``products`` within the ``Promotion`` resource to properly retain ``type`` and ``sub_type`` fields after being parsed into a dictionary.

0.1.44 (2015-05-22)
-------------------

* Changed default `cache_backend` to use `gapipy.cache.NullCache`. Previously, `SimpleCache` was the default and led to confusion in production environments, specifically as to why resources were not matching the API output. Now, by default, to get any caching from gapipy you must explicitly set it.

0.1.43 (2015-04-29)
-------------------

* Fixed `Place` init with empty admin_divisions


0.1.42 (2015-04-29)
-------------------

* Added `description` to `TourCategory` resource.

0.1.41 (2015-04-14)
-------------------

* Added `DepartureComponent` resource. See the [official G API documentation for details](https://developers.gadventures.com/docs/departure_component.html)

0.1.40 (2015-04-06)
-------------------

* Added `deposit` to `DepartureService` model

0.1.39 (2015-03-31)
-------------------

* Refactor ``APIRequestor._request``. While this should not change existing functionality, it is now possible to override specific methods on ``APIRequestor`` if needed.


0.1.38 (2015-03-23)
-------------------

* Fixed: Due to inconsistencies in the G API with regards to nested resources, the `fetch` function was modified to use the raw data from the API, rather than a specific set of allowed fields.

0.1.37 (2015-03-23)
-------------------

* Fixed: Iterating over ``products`` within the ``promotions`` object now works as expected. Previously, accessing the ``products`` attribute would result in a Query object with incorrect parameters.

0.1.36 (2015-03-17)
-------------------

* Support free to amount price range formatting (e.g. Free-10CAD)

0.1.35 (2015-03-12)
-------------------

* Added `duration_min` & `duration_max` to `ActivityDossier` model

0.1.34 (2015-03-11)
-------------------

* Added `OptionalActivity` model
* All Dossiers with `details`:
  * Now represented as list of `DossierDetail` models
  * Added convenience methods for retrieving specific details
* `ItineraryComponent` and `ActivityDossier` use new `Duration` model
  for their `duration` field/property
* Added `duration_label` and `location_label` to `ItineraryComponent`
* Added `duration_label`, `price_per_person_label`, and `price_per_group_label`
  to `ActivityDossier`


0.1.33 (2015-03-02)
-------------------

* Added `name` field to the Itinerary resource.


0.1.32 (2015-02-18)
-------------------

* Changed cache key creation to account for `GAPI_LANGUAGE` when the environment variable is set.

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

* Bug fix to correctly send ``Content-Type: application/json`` in POST, PUT, or PATCH.

0.1.27 (2015-01-19)
-------------------

* Update ``DepartureService`` object to contain a reference to its ``Itinerary``

0.1.26 (2015-01-14)
-------------------

* Normalize API request headers, to promote caching.

0.1.25 (2015-01-09)
-------------------

* Added ``ActivityDossier`` and ``AccommodationDossier`` resources, as well as references to it from ``Activity`` and ``Accommodation``.

0.1.24 (2015-01-07)
-------------------

* Added ``PlaceDossier`` resource, as well as reference to it from ``Place``

0.1.22 (2014-12-12)
-------------------

* Added ``advertised_departures`` to ``TourDossier``

0.1.21 (2014-11-26)
-------------------

* Fixed a bug with promotions on a Price object. When promotions were accessed, gapipy would query for all promotions, rather than returning the inline list.

0.1.20 (2014-11-20)
-------------------

* Departure resource is now listable via filters.

0.1.19 (2014-11-17)
-------------------

* Fixed a bug with `RedisCache.is_cached` where it would not use the set `key_prefix` when checking for existence in cache. Effectively, it would always return False

0.1.18 (2014-11-12)
-------------------

* When setting a date_field, initiate it as a `datetime.date` type.

0.1.17 (2014-11-07)
-------------------

* Deprecated `RedisHashCache` from cache backends available by default. Was not well tested or reliable.

0.1.16 (2014-10-28)
---------------------

* Fixed a bug where if a model field received `null` as a value, it would fail. Now,
    if the result is `null`, the model field will have an appropriate `None` value.

0.1.15 (2014-10-23)
---------------------

* Fix a bug in the DepartureRoom model. The `price_bands` attribute is now
  properly set.


0.1.14 (2014-10-22)
---------------------

* Fixed a bug where AgencyDocument was not included in the code base.


0.1.13 (2014-10-21)
---------------------

* Add ``latitude``, ``longitude``, and ``documents`` to the ``Agency`` resource.

0.1.12 (2014-10-20)
---------------------

* ``date_created`` on the ``Agency`` resource is correctly parsed as a local time.

0.1.11 (2014-10-15)
---------------------

* Improve the performance of ``Resource.fetch`` by handling cache get/set.

0.1.10 (2014-10-09)
---------------------

* Fix a bug in AccommodationRoom price bands. The `season_dates` and
  `blackout_dates` attributes are now properly set.


0.1.9 (2014-09-23)
---------------------

* Add `iso_639_3` and `iso_639_1` to `Language`

0.1.8 (2014-09-17)
---------------------

* Remove the `add_ons` field in `Departure`, and add `addons`.


0.1.7 (2014-08-22)
---------------------

* Fix a bug when initializing AccommodationRoom from cached data.

0.1.6 (2014-08-19)
---------------------

* Add Query.purge_cached

0.1.5 (2014-07-29)
---------------------

* Add `details` field to the list of `incomplete_requirements` in a `DepartureService`.

0.1.4 (2014-07-21)
---------------------

* Removed sending of header `X-HTTP-Method-Override: PATCH` when the update
  command is called. Now, when `.save(partial=True)` is called, the
  correct PATCH HTTP method will be sent with the request.

0.1.3 (2014-07-18)
------------------

* Return ``None`` instead of raising a HTTPError 404 exception when fetching a
  non-existing resource by id.
* Added ability to create resources from the Query objects on the client
  instance (for example, ``api.customers.create({'name': {'legal_first_name': 'Pat', ...}, ...})``)

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
