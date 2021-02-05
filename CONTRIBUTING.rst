.. :contributing:

Contributing
============

.. note:: Ensure a Python 2 environment

1. Run ``pip install -r requirements-dev.txt`` to setup dev dependencies.


2. Always make your changes in a branch and to submit a PR.

   $ git checkout master
   $ git pull
   $ git checkout -b feature-branch-name


3. Once the PR has been accepted/merged into the ``master`` branch, follow
   these steps.

   $ cd /path/to/gapipy
   $ git checkout master
   $ git pull origin master


Modify the following files:

   * ``gapipy/__init__.py``

      * increment the ``__version__`` variable
      * NOTES on incrementing the version:

         * style ``major.minor.patch``
         * update ``major`` when we switch to ``python3`` only support
         * update ``minor`` if there is some breaking change or adding a New resource
         * update ``patch`` when adding new fields, fixing bugs introduced by a minor release
         * See `semver.org <https://semver.org>`_ for more information.

   * update ``HISTORY.rst``

      * update this file with the new ``version`` & ``date``
      * Add some brief notes describing the changes


4. Use ``make dist`` to check the generated long_description rST file is valid.

   .. note::

      * ignore ``warning: no previously-included files matching`` messages
      * as long as you get a ``Checking dist/gapipy-a.b.c.tar.gz: PASSED``
        message, you are good! If not, fix the errors as dictated in the output

   Example output when running ``make dist``:

   .. code-block:: sh

      $ make dist
      warning: no previously-included files matching '*' found under directory 'tests'
      warning: no previously-included files matching '__pycache__' found under directory '*'
      warning: no previously-included files matching '.eggs' found under directory '*'
      warning: no previously-included files matching '*.py[co]' found under directory '*'
      total 152
      -rw-r--r--  1 user  group  76276  5 Feb 02:53 gapipy-2.28.0.tar.gz
      Checking dist/gapipy-2.28.0.tar.gz: PASSED


5. Push the new commit

   * Use ``Release a.b.c (YYYY-MM-DD)`` format for the commit title. Optionally
     add a description that matches the changes made to ``HISTORY.rst``


6. Create a release on github with the following description (This will be
   tagged to the ``Release`` commit and not the PR/change commit)

   .. code-block:: md

      # Version a.b.c

      PR: #123

      A brief description describing the changes
      * bullet points
      * make for easy reading


7. Release!

   $ make release

🙌 Thanks for helping! 🙌
