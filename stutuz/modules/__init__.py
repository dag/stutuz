#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from werkzeug import import_string


def mod(path):
    return import_string('stutuz.modules.' + path + '.mod')


MOUNTS = [('/export', mod('relvlast.export')),
          ('/api/1', mod('relvlast.api')),
         ]
