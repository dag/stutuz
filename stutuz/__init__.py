#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from logbook import NestedSetup
from flask import Flask, request, Markup
from babel.dates import format_datetime
from flaskext.babel import Babel, get_locale

from stutuz.extensions import genshi, db
from stutuz.converters import converters
from stutuz.modules import MOUNTS


def create_app(config=None):

    app = Flask(__name__)

    app.config.from_object('stutuz.configs')
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('STUTUZ_CONFIG', silent=True)

    def _format_datetime(datetime, format='short'):
        return format_datetime(datetime, format, locale=get_locale())

    @app.context_processor
    def global_context():
        return dict(locale=get_locale(),
                    format_datetime=_format_datetime,
                    Markup=Markup,  # Flask's seems to be superior to Genshi's
                   )

    handlers = app.config.get('LOGBOOK_HANDLERS')
    with NestedSetup(handlers):
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

        app.url_map.converters.update(converters)
        for url_prefix, module in MOUNTS:
            app.register_module(module, url_prefix=url_prefix)

        return app
