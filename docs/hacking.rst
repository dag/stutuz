Hacking on stutuz
=================

.. highlight:: bash


Forking the code
----------------

Prerequisites:

* Git
* `hub <http://github.com/defunkt/hub>`_

::

    hub clone dag/stutuz
    cd stutuz
    hub fork


Setting up a development instance
---------------------------------

Prerequisites:

* Python 2.6 or 2.7
* `virtualenv <http://virtualenv.openplans.org/>`_
* `virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_
* Headers for libxml2 and libxslt

On Ubuntu 10.10 you can install all of these with::

    sudo apt-get install virtualenvwrapper libxslt-dev

Next, we'll create a virtual Python environment to set it all up in::

    mkvirtualenv --no-site-packages stutuz
    ./setup.py develop


Working with our development instance
-------------------------------------

Run the tests::

    stutuzctl runtests

Start the development server::

    stutuzctl runserver

When you're done you might want to get out of the environment::

    deactivate

And the next time you need it, run::

    workon stutuz


Technical details
-----------------

* `Flask <http://flask.pocoo.org/docs/>`_ is used for the HTTP side
* `Werkzeug <http://werkzeug.pocoo.org/documentation/0.6.2/>`_ is primarily
  used by Flask but sometimes we use it directly
* `Genshi <http://genshi.edgewall.org/wiki/Documentation/0.6.x/xml-templates.html>`_
  is used for HTML templating
* `ZODB <http://zodb.org/>`_ is used for data persistence


Contributing
------------

First of all: *Don't panic!* An unsuccessful attempt at contributing has more
potential to lead to a successful contribution than no attempt at all. It
can also help me improve this documentation!

Some suggestions:

* Follow the `Style Guide for Python code <http://www.python.org/dev/peps/pep-0008/>`_
* Add unit tests for new code and make sure all tests pass before you commit
* Write docstrings where they make sense, with
  `Sphinx <http://sphinx.pocoo.org/contents.html>`_ markup

There are some tools you can use to check your code (but beware of false
positives - no need to be fanatic)::

    pip install pep8 pyflakes

Check the code style::

    pep8 stutuz/

Look for missing or unused imports/variables/etc::

    pyflakes stutuz/

And finally: Have fun!
