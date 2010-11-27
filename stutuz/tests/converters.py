#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import current_app

from stutuz.tests.tools import flask_tests
from stutuz.extensions import db


suite = flask_tests()


@suite.test
def lang(client):
    """The lang converter matches known language codes"""

    @current_app.route('/_test/<lang:code>')
    def lang_code(code):
        return db['languages'][code]

    response = client.get('/_test/en')
    assert response.status_code == 404

    response = client.get('/_test/eng')
    assert response.data == 'English'
