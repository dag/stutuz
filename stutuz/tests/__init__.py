#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from attest import Tests


suite = lambda mod: 'stutuz.tests.' + mod + '.suite'

all = Tests([suite('schemata'),
             suite('models'),
             suite('api'),
             suite('zodb'),
             suite('export'),
             suite('utils'),
            ])
