#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from stutuz.tests import TestBase
from stutuz.extensions import db
from stutuz.models import Definition, Root


class Export(TestBase):

    def test_xml(self):
        """XML export contains the right elements and attributes"""

        cipra = Root(id='cipra', affixes=['cip'])
        cipra.history('eng').revise(object=Definition(
            definition='x1 is a test...',
            notes='Also examination, proxy measure, validation...'
        ))

        with db() as root:
            root['entries']['cipra'] = cipra

        response = self.client.get('/export/eng.xml')

        xpaths = (
            '/dictionary/direction[@from="Lojban"][@to="English"]',
            '//valsi[@word="cipra"][@type="gismu"]/rafsi = "cip"',
            '//definition = "x1 is a test..."',
            '//notes = "Also examination, proxy measure, validation..."'
        )

        for path in xpaths:
            self.assert_xml(response, path)
