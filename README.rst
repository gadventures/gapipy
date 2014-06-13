===============================
G API Python Client
===============================

A client for the G Adventures REST API (https://developers.gadventures.com)

* GitHub Repository: https://github.com/gadventures/gapipy/
* Documentation: http://gapipy.readthedocs.org.
* Free software: MIT license


Quick Start
-----------

    >>> from gapipy import Client
    >>> api = Client(application_key='MY_SECRET_KEY')
    >>> tour = api.tours.get(21346)
    >>> tour.product_line
    u'PPP'
    >>> tour.departures.count()
    105
    >>> dossier = tour.tour_dossier
    >>> dossier.name
    u'Peru Panorama'
    >>> tour.get_brief_itinerary()[:2]
    [{'body': u'Arrive at any time.', 'label': u'Day 1 Lima'},
     {'body': u'Fly to Juliaca and transfer to Puno.  Visit the floating Islands of Uros and take a guided tour of Lake Titicaca with a homestay in a small village.   Optional visit to Sillustani burial site.',
      'label': u'Days 2-4 Puno/Lake Titicaca (1B,1L,1D)'}]


Resources
---------

Resource objects are instantiated from python dictionaries created from JSON
data. The fields are parsed and converted to python objects as specified in the
resource class.

A nested resource will only be instantiated when its corresponding attribute is
accessed in the parent resource.

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

``gapipy.cache.SimpleCache``
    A simple in-memory cache for single process environments and is not
    thread safe.

``gapipy.cache.RedisCache``
    A key-value cache store using Redis as a backend. Currently there is no
    simple way to adjust the cache config when using the client.

``gapipy.cache.NullCache``
    A cache that doesn't cache.

Since the cache backend is defined by a python module path, you are free to use
a cache backend outside of this project.


Dependencies
------------

The only dependency needed to use the client is requests_.

.. _requests: http://python-requests.org
