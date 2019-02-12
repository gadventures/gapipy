===============================
G API Python Client
===============================

.. image:: https://badge.fury.io/py/gapipy.svg
    :target: http://badge.fury.io/py/gapipy

.. image:: https://travis-ci.com/gadventures/gapipy.svg?branch=master
    :target: https://travis-ci.com/gadventures/gapipy

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

All queries support the ``get``, ``create`` and ``options`` methods. The other methods are
only supported for queries whose resources are listable.

``options()``
    Get the options for a single resource

``get(resource_id, [headers={}])``
    Get a single resource; optionally passing in a dictionary of header
    values.

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
* http://urllib3.readthedocs.io/en/latest/reference/index.html#module-urllib3.connectionpool


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

In addition to running the test suite against your local Python interpreter, you
can run tests using `Tox <http://tox.testrun.org>`_. Tox allows the test suite
to be run against multiple environments, or in this case, multiple versions of
Python. Install and run the ``tox`` command from any place in the gapipy source
tree. You'll want to export your G API application key as well::

  $ export GAPI_APPLICATION_KEY=MY_SECRET_KEY
  $ pip install tox
  $ tox

Tox will attempt to run against all environments defined in the ``tox.ini``. It
is recommended to use a tool like `pyenv <https://github.com/yyuu/pyenv>`_ to
ensure you have multiple versions of Python available on your machine for Tox to
use.


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


Contributing
------------

1. Always make your changes in a branch and submit a PR

2. Once the PR has been completed and the changes pulled into the `master` branch. Do the following on your local box:

.. code-block:: bash

   $> cd /path/to/gapipy
   $> git checkout master
   $> git pull origin master


Then, modify the following files:

* ``gapipy/__init__.py``

  * update the ``__version__`` variable
  * NOTES on incrementing the version:

    * ``major.minor.patch``
    * update ``major`` only when we switch to ``python3`` only support
    * update ``minor`` if there is some breaking change or adding a New resource
    * update ``patch`` when adding new fields, fixing minor bugs

    * See `semver.org <https://semver.org>`_ for more information.

* ``HISTORY.rst``

  * update this file with the new ``version`` & ``date`` (x.x.x)
  * Add some brief notes describing the changes

3. Push the new commit

* Use ``Release: x.x.x (YYYY-MM-DD)`` format for the commit title. Optionally add a description that matches the changes to ``HISTORY.rst``

4. Create a release on github with the following description (This will be tagged to the ``version bump`` commit and not the PR commit)

.. code-block:: md

    # Version 2.x.x

    PR: #123

    A brief description describing the changes
    * bullet points
    * make for easy reading


5. Back to your local box

* Please don't use `python setup.py sdist upload` as it seems to be having an issue pushing. We will now deploy to PyPi following these two steps

* Note: If you don't have `twine` you can install it using `pip install twine`

.. code-block:: bash

    $> python setup.py sdist
    # this will create `gapipy-x.x.x.tar.gz` in the `./dist` directory

    $> twine upload dist/gapipy-x.x.x.tar.gz
    # this will upload & create the release pypi


Thanks for helping!
