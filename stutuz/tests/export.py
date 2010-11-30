#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from stutuz.tests.tools import flask_tests, assert_xml
from stutuz.extensions import db
from stutuz.models import Definition, Root


suite = flask_tests()


@suite.test
def xml(client):
    """XML export contains the right elements and attributes"""

    cipra = Root(id='cipra', affixes=['cip'])
    cipra.history('en').revise(object=Definition(
        definition='x1 is a test...',
        notes='Also examination, proxy measure, validation...'
    ))

    with db() as root:
        root['entries']['cipra'] = cipra

    response = client.get('/export/en.xml')

    xpaths = (
        '/dictionary/direction[@from="Lojban"][@to="English"]',
        '//valsi[@word="cipra"][@type="gismu"]/rafsi = "cip"',
        '//definition = "x1 is a test..."',
        '//notes = "Also examination, proxy measure, validation..."'
    )

    for path in xpaths:
        assert_xml(response, path)
