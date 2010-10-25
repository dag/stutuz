Configuration
=============

Configurations for stutuz are Python modules defining a set of constants
in the top level. These modules reside in the ``stutuz.configs`` package.

First, the ``stutuz.configs`` package itself is loaded for defaults.
Second, the config module passed to :func:`stutuz.create_app` is loaded.
For :command:`stutuzctl` this defaults to ``stutuz.configs.development``
but it can be overridden with ``--config / -c``. The tests run with
``stutuz.configs.testing``. Lastly, if the environment variable
:envvar:`STUTUZ_CONFIG` is defined, it is also loaded.

The configuration system is used for options that might differ between
deployments and development environments.


Options
-------

.. describe:: DEBUG

   Whether to enable the interactive debugger.


.. describe:: TESTING

   Whether we're running in test mode.


.. describe:: SECRET_KEY

   Secret key used for signing cookies.


.. describe:: MIDDLEWARES

   List of WSGI middlewares to apply to the application.


.. describe:: LOGBOOK_HANDLERS

   List of Logbook handlers used in a :class:`~logbook.NestedSetup`.


.. describe:: ZODB_STORAGE

   Callable returning a ZODB storage.
