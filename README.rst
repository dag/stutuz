Prototypical foundation for a Lojban web infrastructure with a focus on Jbovlaste 2.
====================================================================================

(From the affix forms of *stuzi* as a *cmevla*, because it's not really
a *stuzi* (more like a *ciste* or a *tcana*) and because Robin loves
affix-form *cmevla*. Also, *lojbo tcana* was sort of already taken.)


So... What is this, really?
---------------------------

Not really anything - yet. I'm laying the groundwork for what hopefully will
end up being the next `jbovlaste <http://jbovlaste.lojban.org/>`_, also known
as *relvlast* and JVS2, or really any web application the community might need.
The idea is to have a solid foundation to build anything on easily.

As for Jbovlaste 2, my thinking is that it's better to start *now* building
*something* than endlessly discuss how to design it first. As we perfect the
design, it should be easy to adapt the implementation because it is built
with modern technologies and test driven development.


Great! So when can I use it?
----------------------------

Not in quite some time! Just reimplementing *jbovlaste* from scratch is a
non-trivial undertaking, and we're not even sure yet how we want to *redesign*
it. In fact, I'm working under the assumption that the Lojban server will
support Python 2.6 by the time this is deployed, something which requires
Debian to release their next stable version and Robin to update the machine.
Even *then* it might not be usable yet.


Setting up a development instance
---------------------------------

Prerequisites:

* Python 2.6 or 2.7
* `virtualenv <http://virtualenv.openplans.org/>`_
* `virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_

On Ubuntu 10.10 you can install all of these with::

    sudo apt-get install virtualenvwrapper

Next, we'll create a virtual Python environment to set it all up in::

    mkvirtualenv --no-site-packages stutuz
    ./setup.py develop


Working with our development instance
-------------------------------------

Run the tests::

    ./setup.py test

Start the development server::

    ./manage.py runserver

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

Check to code style::

    pep8 stutuz/

Look for missing or unused imports/variables/etc::

    pyflakes stutuz/

And finally: Have fun!
