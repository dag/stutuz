#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import re
from functools import partial

from flaskext.testing import TestCase

from stutuz import create_app


class TestBase(TestCase):

    def create_app(self):
        return create_app('stutuz.configs.testing')

    def __getattr__(self, name):
        name = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), name)
        return partial(getattr(TestCase, name), self)
