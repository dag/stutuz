#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import os

import logbook
from logbook.more import ColorizedStderrHandler
from logbook.notifiers import create_notification_handler
from ZODB.FileStorage import FileStorage


DEBUG = True
SECRET_KEY = 'stutuz-development'


class ThemedStderrHandler(ColorizedStderrHandler):

    def get_color(self, record):
        case = lambda x: record.level >= x
        if case(logbook.ERROR):
            return 'darkred'
        elif case(logbook.NOTICE):
            return 'darkyellow'
        elif case(logbook.INFO):
            return 'darkgray'
        return 'black'


LOGBOOK_HANDLERS = [
    ThemedStderrHandler(),
]

try:
    notifier = create_notification_handler(level=logbook.WARNING)
except RuntimeError:
    pass
else:
    notifier.bubble = True
    LOGBOOK_HANDLERS.append(notifier)

try:
    os.makedirs('var/db')
except OSError:
    pass

ZODB_STORAGE = lambda: FileStorage('var/db/development.fs')
