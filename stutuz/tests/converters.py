#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import current_app
from babel import Locale

from stutuz.tests.tools import flask_tests


suite = flask_tests()


@suite.test
def lang(client):
    """The lang converter matches known language codes"""

    @current_app.route('/_test/<lang:code>')
    def lang_code(code):
        return Locale(code).english_name

    response = client.get('/_test/eng')
    assert response.status_code == 404

    response = client.get('/_test/en')
    assert response.data == 'English'
