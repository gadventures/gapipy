===============================
G API Python Client
===============================

.. image:: https://badge.fury.io/py/gapipy.svg
    :target: http://badge.fury.io/py/gapipy

.. image:: https://travis-ci.org/gadventures/gapipy.svg?branch=master
    :target: https://travis-ci.org/gadventures/gapipy

A client for the G Adventures REST API (https://developers.gadventures.com)

* GitHub Repository: https://github.com/gadventures/gapipy/
* Documentation: http://gapipy.readthedocs.org.
* Free software: MIT license


Quick Start
-----------

.. code-block:: python

    >>> from gapipy import Client
    >>> api = Client(application_key='MY_SECRET_KEY')

    >>> # Get a resource by id
    >>> tour = api.tours.get(24309)
    >>> tour.product_line
    u'AHEH'
    >>> tour.departures.count()
    134
    >>> dossier = tour.tour_dossier
    >>> dossier.name
    u'Essential India'
    >>> itinerary = dossier.structured_itineraries[0]
    >>> {day.day: day.summary for day in itinerary.days[:3]}
    {1: u'Arrive at any time. Arrival transfer included through the G Adventures-supported Women on Wheels project.',
    2: u'Take a morning walk through the city with a young adult from the G Adventures-supported New Delhi Streetkids Project. Later, visit Old Delhi, explore the spice markets, and visit Jama Masjid and Connaught Place.',
    3: u"Arrive in Jaipur and explore this gorgeous 'pink city'."}

    >>> # Create a new resource
    >>> booking = api.bookings.create({'currency': 'CAD', 'external_id': 'abc'})

    >>> # Modify an existing resource
    >>> booking.external_id = 'def'
    >>> booking.save()


Resources
---------

Resource objects are instantiated from python dictionaries created from JSON
data. The fields are parsed and converted to python objects as specified in the
resource class.

A nested resource will only be instantiated when its corresponding attribute is
accessed in the parent resource. These resources may be returned as a ``stub``,
and upon access of an attribute not present, will internally call ``.fetch()``
on the resource to populate it.

A field pointing to the URL for a collection of a child resources will hold a
``Query`` object for that resource. As for nested resources, it will only be
instantiated when it is first accessed.


Queries
-------

A Query for a resource can be used to fetch resources of that type (either a
single instance or an iterator over them, possibly filtered according to  some
conditions). Queries are roughly analogous to Django's QuerySets.

An API client instance has a query object for each available resource
(accessible by an attribute named after the resource name)

Methods on Query objects
========================

All queries support the ``get`` and ``create`` methods. The other methods are
only supported for queries whose resources are listable.

``get(resource_id)``
    Get a single resource.

``create(data)``
    Create an instance of the query resource using the given data.

``all([limit=n])``
    Generator over all resources in the current query. If ``limit`` is a
    positive integer ``n``, then only the first ``n`` results will be returned.

``filter(field1=value1, [field2=value2, ...])``
    Filter resources on the provided fields and values. Calls to ``filter`` can
    be chained.

``count()``
    Return the number of resources in the current query (by reading the
    ``count`` field on the response returned by requesting the list of
    resources in the current query).

Caching
-------

``gapipy`` can be configured to use a cache to avoid having to send HTTP
requests for resources it has already seen. Cache invalidation is not
automatically handled: it is recommended to listen to G API webhooks_ to purge
resources that are outdated.

.. _webhooks: https://developers.gadventures.com/docs/webhooks.html

By default, ``gapipy`` will use the cached data to instantiate a resource, but
a fresh copy can be fetched from the API by passing ``cached=False`` to
``Query.get``. This has the side-effect of recaching the resource with the
latest data, which makes this a convenient way to refresh cached data.

Caching can be configured through the ``cache_backend`` and ``cache_options``
settings. ``cached_backend`` should be a string of the fully qualified path to
a cache backend, i.e. a subclass of ``gapipy.cache.BaseCache``. A handful of
cache backends are available out of the box:

* ``gapipy.cache.SimpleCache``
    A simple in-memory cache for single process environments and is not
    thread safe.

* ``gapipy.cache.RedisCache``
    A key-value cache store using Redis as a backend.

* ``gapipy.cache.NullCache`` (Default)
    A cache that doesn't cache.

Since the cache backend is defined by a python module path, you are free to use
a cache backend that is defined outside of this project.


Connection Pooling
------------------

We use the ``requests`` library, and you can take advantage of the provided
connection pooling options by passing in a ``'connection_pool_options'`` dict
to your client.

Values inside the ``'connection_pool_options'`` dict of interest are as
follows:

* Set ``enable`` to ``True`` to enable pooling. Defaults to ``False``.
* Use ``number`` to set the number of connection pools to cache.
  Defaults to 10.
* Use ``maxsize`` to set the max number of connections in each pool.
  Defaults to 10.
* Set ``block`` to ``True`` if the connection pool should block and wait
  for a connection to be released when it has reached ``maxsize``. If
  ``False`` and the pool is already at ``maxsize`` a new connection will
  be created without blocking, but it will not be saved once it is used.
  Defaults to ``False``.

See also:

* http://www.python-requests.org/en/latest/api/#requests.adapters.HTTPAdapter
* http://urllib3.readthedocs.org/en/latest/pools.html#urllib3.connectionpool.HTTPConnectionPool


Dependencies
------------

The only dependency needed to use the client is requests_.

.. _requests: http://python-requests.org

Testing
-------

Running tests is pretty simple. We use `nose` as the test runner. You can
install all requirements for testing with the following::

    $ pip install -r requirements-testing.txt

Once installed, run unit tests with::

    $ nosetests -A integration!=1

Otherwise, you'll want to include a GAPI Application Key so the integration
tests can successfully hit the API::

    $ export GAPI_APPLICATION_KEY=MY_SECRET_KEY; nosetests

Fields
------

* ``_model_fields`` represent dictionary fields like so:

Note: ``_model_fields = [('address', Address)]`` and ``Address`` subclasses ``BaseModel``

.. code-block:: python

    "address": {
        "street": "19 Charlotte St",
        "city": "Toronto",
        "state": {
          "id": "CA-ON",
          "href": "https://rest.gadventures.com/states/CA-ON",
          "name": "Ontario"
        },
        "country": {
          "id": "CA",
          "href": "https://rest.gadventures.com/countries/CA",
          "name": "Canada"
        },
        "postal_zip": "M5V 2H5"
      }


* ``_model_collection_fields`` represent a list of dictionary fields like so:

Note: ``_model_collection_fields = [('emails', AgencyEmail),]`` and ``AgencyEmail`` subclasses ``BaseModel``

.. code-block:: python

    "emails": [
        {
          "type": "ALLOCATIONS_RELEASE",
          "address": "g@gadventures.com"
        },
        {
          "type": "ALLOCATIONS_RELEASE",
          "address": "g2@gadventures.com"
        }
      ]

* ``_resource_fields`` refer to another ``Resource``

Thanks for helping!
