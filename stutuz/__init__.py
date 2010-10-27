#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from logbook import Logger, NestedSetup
from flask import Flask
from flaskext.genshi import Genshi
from flaskext.zodb import ZODB, PersistentMapping


logger = Logger(__name__)
genshi = Genshi()
db = ZODB()


@db.init
def set_defaults(root):
    if 'languages' not in root:
        root['languages'] = PersistentMapping({'eng': 'English',
                                               'jbo': 'Lojban'})


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object('stutuz.configs')
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('STUTUZ_CONFIG', silent=True)

    handlers = app.config.get('LOGBOOK_HANDLERS')
    with NestedSetup(handlers):
        for extension in genshi, db:
            extension.init_app(app)

        for middleware in app.config.get('MIDDLEWARES', ()):
            app.wsgi_app = middleware(app.wsgi_app)

        return app
