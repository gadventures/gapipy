.. :changelog:

History
-------

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
