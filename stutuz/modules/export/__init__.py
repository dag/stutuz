#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import Module
from flaskext.genshi import render_response

from stutuz.extensions import db


mod = Module(__name__)


@mod.route('/<lang:language>.xml')
def xml(language):
    return render_response('export/export.xml', {
        'langcode': language,
        'language': db['languages'][language],
        'entries': (e for e in db['entries'].itervalues()
                      if e.history(language))
    })
