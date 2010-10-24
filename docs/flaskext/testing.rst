Testing
=======

.. module:: flaskext.testing

* `Full documentation <http://packages.python.org/Flask-Testing/>`_
* `Assertions inherited from unittest <http://docs.python.org/library/unittest.html#unittest.TestCase.assertTrue>`_

With the stutuz :class:`~stutuz.tests.TestBase` class we can write
all assertions in ``snake_case``. We also have all the new changes in
Python 2.7 unittesting even in 2.6, due to depending on unittest2.


API
---

.. autoclass:: TestCase
   :members: assert_200, assert_401, assert_403, assert_404, assert_405, assert_redirects, assert_status
