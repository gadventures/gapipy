.. :changelog:

History
-------

0.1.0 (2014-06-20)
---------------------

* First release on PyPI.

0.1.1 (2014-06-27)
---------------------

* Use setuptools find_packages

0.1.2 (2014-07-14)
---------------------

* Added cache options 

0.1.3 (2014-07-21)
---------------------

* Removed sending of header `X-HTTP-Method-Override: PATCH` when the update
    command is called. Now, when `.save(partial=True)` is called, the
    correct PATCH HTTP method will be sent with the request.
