Script
======

* `Full documentation <http://packages.python.org/Flask-Script/>`_

In stutuz we run our script manager with :command:`stutuzctl`
and the code is in :file:`stutuz/manage.py`.

.. program:: stutuzctl

.. option:: runserver

   Starts a development server.

.. option:: runtests

   Runs the full test suite for stutuz.

.. option:: shell

   An interactive Python console with some stutuz objects included.
   Loads :command:`bpython` if installed:

   .. code-block:: bash

      easy_install bpython


API
---

.. automodule:: flaskext.script
   :members:
