Data models in stutuz
=====================

.. module:: stutuz.models


User accounts
-------------

.. autoclass:: Account(username=None, password=None)
   :members:

.. autoclass:: Users({username: Account()…})
   :members:


Revisions
---------

.. autoclass:: History([Revision()…])
   :members:

.. autoclass:: Revision(author=Account(), comment=None, object=None)
   :members:
