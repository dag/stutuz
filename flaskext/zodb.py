#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from contextlib import contextmanager
from datetime import datetime
from uuid import uuid4

from werkzeug import cached_property, LocalProxy
from ZODB.DB import DB
from flask import g, current_app
import transaction
from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping


class ZODB(object):
    """ZODB extension for Flask: persistence of native Python objects.

    Basic setup::

        from ZODB.FileStorage import FileStorage
        from flask import Flask, redirect, render_template_string
        from flaskext.zodb import ZODB

        ZODB_STORAGE = lambda: FileStorage('app.fs')

        app = Flask(__name__)
        app.config.from_object(__name__)
        db = ZODB(app)

        @app.route('/')
        @app.route('/<message>')
        def index(message=None):
            if message is not None:
                db['message'] = message
                return redirect('/')
            return render_template_string('Latest message: {{ message }}',
                                          message=db['message'])

    During requests the ``db`` object can be used as a ``dict`` for setting,
    getting and deleting keys. For other operations, ``db.root`` implements
    the full ``dict`` interface.

    Outside of requests, the object can be used as a context manager if
    called, yielding the root object to be used inside the context.
    See :meth:`__call__`.

    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    @cached_property
    def db(self):
        return DB(self.app.config['ZODB_STORAGE']())

    @property
    def connection(self):
        """Request-local database connection."""
        return g._zodb_connection

    @connection.setter
    def connection(self, new):
        g._zodb_connection = new

    @property
    def root(self):
        """Root object for the request-local connection."""
        return self.connection.root()

    def init_app(self, app):
        assert 'ZODB_STORAGE' in app.config, \
               'ZODB_STORAGE must be configured.'
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['zodb'] = self

        @app.before_request
        def open_db():
            self.connection = self.db.open()
            transaction.begin()

        @app.after_request
        def close_db(response):
            transaction.commit()
            self.connection.close()
            return response

    def __setitem__(self, key, value):
        """Set an item in the request-local root object."""
        self.root[key] = value

    def __getitem__(self, key):
        """Get an item in the request-local root object."""
        return self.root[key]

    def __delitem__(self, key):
        """Delete an item in the request-local root object."""
        del self.root[key]

    @contextmanager
    def __call__(self):
        """Transactional context, for database access outside of requests.

        ::

            with db() as root:
                root['this'] = 'is committed at the end of the context.'

        """
        try:
            connection = self.db.open()
            transaction.begin()
            yield connection.root()
        finally:
            transaction.commit()
            connection.close()


class Factory(object):
    """Set a :class:`Model` attribute with a callable on instantiation.
    Useful for delaying initiation of mutable or dynamic objects.

    ::

        class Dice(Model):
            side = Factory(random.randint, 1, 6)

    ::

        >>> Dice()
        Dice(side=3)
        >>> Dice()
        Dice(side=5)

    """

    def __init__(self, callable, *args, **kwargs):
        self.callable = callable
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.callable(*self.args, **self.kwargs)


#: UTC timestamp factory
Timestamp = Factory(datetime.utcnow)

#: UUID4 factory
UUID4 = Factory(uuid4)

#: Factory for :class:`~persistent.list.PersistentList`
List = Factory(PersistentList)

#: Factory for :class:`~persistent.mapping.PersistentMapping`
Mapping = Factory(PersistentMapping)


class Model(Persistent):
    """Convinience model base.

    You can subclass :class:`persistent.Persistent` directly if you prefer,
    but this base provides some conviniences.

    Set attributes in instantiation::

        >>> Model(title='Hello!')
        Model(title='Hello!')
        >> Model(title='Hello!').title
        'Hello!'

    Declare mutable and dynamic attributes in the class definition::

        class Post(Model):
            id = UUID4
            posted_on = Timestamp
            comments = List

    ::

        >>> Post()
        Post(id=UUID('c3f043a8-8f1f-4381-89b3-fd1f35265925'),
             posted_on=datetime.datetime(2010, 10, 20, 15, 42, 34, 138015),
             comments=[])
        >>> type(Post().comments)
        <class 'persistent.list.PersistentList'>

    """

    def __init__(self, **kwargs):
        for name, value in vars(self.__class__).items():
            if isinstance(value, Factory):
                setattr(self, name, value())

        for name, value in kwargs.iteritems():
            try:
                attribute = getattr(self, name)
            except AttributeError:
                attribute = None
            if isinstance(attribute, PersistentList):
                attribute.extend(value)
            elif isinstance(attribute, PersistentMapping):
                attribute.update(value)
            else:
                setattr(self, name, value)

    def __repr__(self):
        attributes = ', '.join('{0}={1!r}'.format(name, value)
            for (name, value) in vars(self).iteritems())
        return '{0}({1})'.format(self.__class__.__name__, attributes)


#: The :class:`ZODB` instance for the current :class:`~flask.Flask`
#: application.
current_db = LocalProxy(lambda: current_app.extensions['zodb'])