#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import re
from functools import partial

from attest import Tests
from flaskext.testing import TestCase
import unittest2
from lxml import etree

from stutuz import create_app


suite = lambda mod: 'stutuz.tests.' + mod + '.suite'
all = Tests([suite('converters')])


class TestBase(TestCase, unittest2.TestCase):

    def setUp(self):
        self.app.preprocess_request()
        if hasattr(self, 'setup'):
            self.setup()

    def tearDown(self):
        self.app.process_response(self.app.response_class())
        if hasattr(self, 'teardown'):
            self.teardown()

    def create_app(self):
        return create_app('stutuz.configs.testing')

    def __getattr__(self, name):
        name = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), name)
        return partial(getattr(unittest2.TestCase, name), self)

    def assert_xml(self, response, xpath):
        """An XPath query on a response returns a True-like result."""
        doc = etree.fromstringlist(response.data)
        self.assert_(doc.xpath(xpath))
