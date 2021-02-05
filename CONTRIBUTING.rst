.. :contributing:

Contributing
============

.. note:: Ensure a Python 2 environment

0. Clone the project

   .. code-block:: sh

      $ git clone git@github.com:gadventures/gapipy


1. Run ``pip install -r requirements-dev.txt`` to setup dev dependencies.


2. Always make your changes in a branch and to submit a PR.

   .. code-block:: sh

      $ git checkout master
      $ git pull
      $ git checkout -b feature-branch-name
      $ git push origin feature-branch-name


3. Once the PR has been accepted/merged into the ``master`` branch, follow
   these steps.

   .. code-block:: sh

      $ cd /path/to/gapipy
      $ git checkout master
      $ git pull origin master


**Modify the following files:**

* Update **gapipy/__init__.py**

   * increment the ``__version__`` variable

   .. note::

      * style ``major.minor.patch``
      * update ``patch`` when adding new fields, fixing bugs introduced by a
        minor release.
      * update ``minor`` if there is some breaking change such as adding a new
        resource, removing fields, adding new behaviour.
      * update ``major`` when we switch to ``Python 3`` only support.
      * See `semver.org <https://semver.org>`_ for more information.

* Update **HISTORY.rst**

   * update this file with the new ``version`` & ``date``
   * Add some brief notes describing the changes.


4. Use ``make dist`` to check the generated long_description rST file is valid.

   .. note::

      * ignore ``warning: no previously-included files matching`` messages.
      * as long as you get a ``Checking dist/gapipy-a.b.c.tar.gz: PASSED``
        message, you are good!
      * If not, fix the errors as dictated in the output, and repeat.

   Example output when running ``make dist``:

   .. code-block:: sh

      $ make dist
      warning: no previously-included files matching '*' found under directory 'tests'
      warning: no previously-included files matching '__pycache__' found under directory '*'
      warning: no previously-included files matching '.eggs' found under directory '*'
      warning: no previously-included files matching '*.py[co]' found under directory '*'
      total 123
      -rw-r--r--  1 user  group  76276  5 Feb 02:53 gapipy-a.b.c.tar.gz
      Checking dist/gapipy-a.b.c.tar.gz: PASSED


5. Push the new *Release* commit

   * Use **Release a.b.c (YYYY-MM-DD)** format for the commit title. Optionally
     add a description that matches the changes made to **HISTORY.rst**.


6. Create a release on github with the following description (This will be
   tagged to the ``Release`` commit and not the PR/change commit)

   .. code-block:: md

      # Release a.b.c (YYYY-MM-DD)

      PR: #123

      A brief description describing the changes
      * bullet points
      * make for easy reading


7. Release!

      $ make release

Thanks for helping!
-------------------