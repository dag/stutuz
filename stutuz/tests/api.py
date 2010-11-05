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

        response = self.client.get('/api/1/entry/?id=donri')
        self.assert_200(response)
        self.assert_equal(response.content_type, 'application/json')
        self.assert_dict_equal({
            'id': 'donri',
            'type': 'gismu',
            'affixes': ['dor', "do'i"]
        }, json.loads(response.data))

        response = self.client.get('/api/1/entry/?id=donri&language=eng')
        self.assert_200(response)
        self.assert_dict_equal({
            'id': 'donri',
            'type': 'gismu',
            'affixes': ['dor', "do'i"],
            'definition': 'x1 is the daytime...',
            'notes': 'See also {nicte}...'
        }, json.loads(response.data))

        response = self.client.get('/api/1/entry/')
        self.assert_equal(response.status_code, 400)
        self.assert_equal(response.content_type, 'application/json')
        self.assert_in('error', json.loads(response.data))

        response = self.client.get('/api/1/entry/?id=undef')
        self.assert_404(response)
        self.assert_equal(response.content_type, 'application/json')
        self.assert_in('error', json.loads(response.data))

        response = self.client.get('/api/1/entry/?id=donri&language=zzz')
        self.assert_equal(response.status_code, 400)
        self.assert_equal(response.content_type, 'application/json')
        self.assert_in('error', json.loads(response.data))
