#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import logbook
from ZODB.DemoStorage import DemoStorage


TESTING = True

LOGBOOK_HANDLERS = [
    logbook.NullHandler(),
    logbook.StderrHandler(level=logbook.WARNING),
]

ZODB_STORAGE = DemoStorage
