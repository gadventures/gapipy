.. :contributing:

Contributing
============

0. Run ``pip install -r requirements-dev.txt`` to setup dev dependencies

1. Always make your changes in a branch and submit a PR

2. Once the PR has been accepted/merged into the ``master`` branch,
   follow these steps on your local box

.. code-block:: bash

    $> cd /path/to/gapipy
    $> git checkout master
    $> git pull origin master

Then, modify the following files:

* ``gapipy/__init__.py``

  * update the ``__version__`` variable
  * NOTES on incrementing the version:

    * ``major.minor.patch``
    * update ``major`` when we switch to ``python3`` only support
    * update ``minor`` if there is some breaking change or adding a New resource
    * update ``patch`` when adding new fields, fixing bugs introduced by a minor release
    * See `semver.org <https://semver.org>`_ for more information.

* ``HISTORY.rst``

  * update this file with the new ``version`` & ``date``
  * Add some brief notes describing the changes

3. Check the generated long_description rST file is valid

.. code-block:: bash

    $> python setup.py sdist
    # this created `gapipy-a.b.c.tar.gz` in the `./dist` directory
    # where a.b.c is the ``__version__`` value

    $> twine check dist/gapipy-a.b.c.tar.gz
    # checks the long-form rST file is valid

    # if there are any errors fix, and repeat

    # example success check
    $> twine check dist/gapipy-a.b.c.tar.gz
    Checking dist/gapipy-a.b.c.tar.gz: PASSED

4. Push the new commit

* Use ``Release a.b.c (YYYY-MM-DD)`` format for the commit title. Optionally add a description that matches the changes to ``HISTORY.rst``

5. Create a release on github with the following description (This will be tagged to the ``version bump`` commit and not the PR commit)

.. code-block:: md

    # Version a.b.c

    PR: #123

    A brief description describing the changes
    * bullet points
    * make for easy reading

6. Back to your local box

.. code-block:: bash

    # build `gapipy-a.b.c.tar.gz` in the `./dist` directory
    # where a.b.c is the ``__version__`` value
    $> python setup.py sdist

    # check the long-form rST file is valid
    $> twine check dist/gapipy-a.b.c.tar.gz

    $> twine upload dist/gapipy-a.b.c.tar.gz
    # this will upload & create the release pypi

Thanks for helping!
