.. :changelog:

History
-------

0.1.46 (2015-06-10)
------------------

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
------------------

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
