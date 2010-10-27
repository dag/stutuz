#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flaskext.genshi import Genshi
from flaskext.zodb import ZODB, PersistentMapping
from stutuz.models import Users


genshi = Genshi()
db = ZODB()


@db.init
def set_defaults(root):
    if 'languages' not in root:
        root['languages'] = PersistentMapping({'eng': 'English',
                                               'jbo': 'Lojban'})
    if 'users' not in root:
        root['users'] = Users()
