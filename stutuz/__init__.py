#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from logbook import Logger, NestedSetup
from flask import Flask
from flaskext.genshi import Genshi
from flaskext.zodb import ZODB


logger = Logger(__name__)
genshi = Genshi()
db = ZODB()


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object('stutuz.configs')
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('STUTUZ_CONFIG', silent=True)

    handlers = app.config.get('LOGBOOK_HANDLERS')
    with NestedSetup(handlers):
        conf = '\n'.join('  {0} = {1!r}'.format(k, v)
                         for (k, v) in app.config.iteritems())
        logger.debug('Loaded app with configuration:\n' + conf)

        for extension in genshi, db:
            logger.debug('Loading extension {0.__module__}'.format(extension))
            extension.init_app(app)

        for middleware in app.config.get('MIDDLEWARES', ()):
            logger.debug('Applying middleware {0.__name__}'.format(middleware))
            app.wsgi_app = middleware(app.wsgi_app)

        return app
