#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import json

from stutuz.extensions import db
from stutuz.models import Root, Definition
from stutuz.tests import TestBase


class API(TestBase):

    def setup(self):
        donri = Root(id='donri', affixes=['dor', "do'i"])
        donri.history('eng').revise(object=Definition(
            definition='x1 is the daytime...',
            notes='See also {nicte}...'
        ))

        with db() as root:
            root['entries']['donri'] = donri

    def test_entry(self):
        """API exposes entries"""

        response = self.client.get('/api/1/entry/donri')
        data = json.loads(response.data)

        self.assert_equal(response.content_type, 'application/json')

        self.assert_dict_equal({
            'id': 'donri',
            'type': 'gismu',
            'affixes': ['dor', "do'i"]
        }, data)

    def test_translation(self):
        """API exposes translations for definitions"""

        response = self.client.get('/api/1/entry/donri?translation=eng')
        data = json.loads(response.data)

        self.assert_dict_equal({
            'id': 'donri',
            'type': 'gismu',
            'affixes': ['dor', "do'i"],
            'definition': 'x1 is the daytime...',
            'notes': 'See also {nicte}...'
        }, data)
