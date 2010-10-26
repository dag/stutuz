Data models in stutuz
=====================

.. module:: stutuz.models


User accounts
-------------

.. autoclass:: Users({username: Account()…})
   :members:

.. autoclass:: Account(username=None, password=None)
   :members:


Revisions
---------

.. autoclass:: History([Revision()…])
   :members:

.. autoclass:: Revision(author=Account(), comment=None, object=None)
   :members:


Entries
-------

.. autoclass:: Definition
   :members:


Bases
^^^^^

.. autoclass:: Entry
   :members:

.. autoclass:: AffixesMixin
   :members:

.. autoclass:: ExperimentalMixin
   :members:


Word types
^^^^^^^^^^

.. autoclass:: Root
   :members:
   :show-inheritance:

.. autoclass:: Compound
   :members:
   :show-inheritance:

.. autoclass:: Particle
   :members:
   :show-inheritance:

.. autoclass:: Loan
   :members:
   :show-inheritance:
