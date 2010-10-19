#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask
from flaskext.genshi import Genshi
from flaskext.zodb import ZODB


genshi = Genshi()
db = ZODB()


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object('stutuz.configs')
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('STUTUZ_CONFIG', silent=True)

    for extension in genshi, db:
        extension.init_app(app)

    return app
