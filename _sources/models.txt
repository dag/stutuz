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
