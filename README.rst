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

All queries support the ``get`` method. The other methods are only supported
for queries whose resources are listable.

``get(resource_id)``
    Get a single resource.

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

A handful of cache backends are available for your use. The cache backend is
configurable by adjusting the ``GAPI_CACHE_BACKEND`` environment variable.

* Use ``cache_options`` when instantiating the Client to override default
  cache client settings.
* Use ``cached=False`` when retrieving a resource to get a fresh copy and
  add it to the cache.
* Use ``Query.is_cached`` to check if a resource is cached
  e.g. ``api.query(resource_name).is_cached(resource_id)``
* Use ``Query.purge_cached`` to purge a resource from the cache.
    e.g. ``api.query(resource_name).purge_cached(resource_id)``

``gapipy.cache.SimpleCache``
    A simple in-memory cache for single process environments and is not
    thread safe.

``gapipy.cache.RedisCache``
    A key-value cache store using Redis as a backend.

``gapipy.cache.NullCache`` (Default)
    A cache that doesn't cache.

Since the cache backend is defined by a python module path, you are free to use
a cache backend outside of this project.


Connection Pooling
------------------

**Known Issue: if you have multiple gapipy clients in the same process using different languages, connection pooling will currently cause some responses to come back in the incorrect language. If you are only using one language, connection pooling will work fine. A fix for this is being investigated.**

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

Thanks for helping!
