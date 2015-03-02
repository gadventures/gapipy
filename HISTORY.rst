.. :changelog:

History
-------

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
