#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import os

from ZODB.FileStorage import FileStorage


DEBUG = True
SECRET_KEY = 'stutuz-development'

try:
    os.makedirs('var/db')
except OSError:
    pass

ZODB_STORAGE = lambda: FileStorage('var/db/development.fs')
