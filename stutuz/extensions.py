#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from logbook import Logger
from flaskext.genshi import Genshi
from flaskext.zodb import ZODB
from BTrees.OOBTree import OOBTree

from stutuz.models import Users


logger = Logger('stutuz')
genshi = Genshi()
db = ZODB()


@db.init
def set_defaults(root):
    if 'languages' not in root:
        root['languages'] = OOBTree({'eng': 'English', 'jbo': 'Lojban'})
    if 'users' not in root:
        root['users'] = Users()
    if 'entries' not in root:
        root['entries'] = OOBTree()
