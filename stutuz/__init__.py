#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from logbook import NestedSetup
from flask import Flask, request, Markup
from flaskext.babel import Babel, get_locale

from stutuz.extensions import genshi, db
from stutuz.schemata import CONVERTERS
from werkzeug import import_string


MODULES = [('/dict', 'relvlast'),
           ('/api/1', 'relvlast.api'),
          ]


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object('stutuz.configs')
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('STUTUZ_CONFIG', silent=True)

    @app.context_processor
    def global_context():
        return dict(locale=get_locale(),
                    Markup=Markup,  # Flask's seems to be superior to Genshi's
                   )

    handlers = NestedSetup(app.config.get('LOGBOOK_HANDLERS'))

    @app.before_request
    def push_handlers():
        handlers.push_thread()

    @app.after_request
    def pop_handlers(response):
        handlers.pop_thread()
        return response

    for extension in genshi, db:
        extension.init_app(app)

    babel = Babel(app)

    @babel.localeselector
    def best_locale():
        if 'locale' in request.args:
            return request.args['locale']
        return request.accept_languages.best_match(
                map(str, babel.list_translations()))

    for middleware in app.config.get('MIDDLEWARES', ()):
        app.wsgi_app = middleware(app.wsgi_app)

    app.url_map.converters.update(CONVERTERS)
    for url_prefix, module in MODULES:
        module = import_string(module).mod
        app.register_module(module, url_prefix=url_prefix)

    return app
