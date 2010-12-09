#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import current_app
from babel import Locale
from attest import Tests, Assert as var

from stutuz import schemata
from stutuz.extensions import db
from tests.tools import flask_tests


forms = flask_tests()

@forms.test
def locale():
    assert var(schemata.Locale('en').validate()).is_(True)
    assert var(schemata.Locale('eng').validate()).is_(False)


@forms.test
def entry():
    with db() as root:
        root['entries']['donri'] = None
    assert var(schemata.Entry('donri').validate()).is_(True)
    assert var(schemata.Entry('claxu').validate()).is_(False)


converters = flask_tests()

@converters.test
def lang(client):
    """The lang converter matches known language codes"""

    @current_app.route('/_test/<lang:code>')
    def lang_code(code):
        return Locale(code).english_name

    response = client.get('/_test/eng')
    assert response.status_code == 404

    response = client.get('/_test/en')
    assert response.data == 'English'


suite = Tests([forms, converters])
