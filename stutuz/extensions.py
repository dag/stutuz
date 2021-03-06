#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from werkzeug import LocalProxy
from flaskext.genshi import Genshi
from genshi.filters import Translator
from flaskext.babel import get_translations
from flaskext.zodb import ZODB
from BTrees.OOBTree import OOBTree

from stutuz.models import Users


current_translations = LocalProxy(get_translations)


genshi = Genshi()
genshi.extensions['html'] = 'html5'

@genshi.template_parsed
def setup_translator(template):
    Translator(current_translations).setup(template)


db = ZODB()

@db.init
def set_defaults(root):
    if 'users' not in root:
        root['users'] = Users()
    if 'entries' not in root:
        root['entries'] = OOBTree()
