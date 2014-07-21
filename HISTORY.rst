.. :changelog:

History
-------

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

* Added cache options


0.1.1 (2014-06-27)
------------------

* Use setuptools find_packages


0.1.0 (2014-06-20)
------------------

* First release on PyPI.
