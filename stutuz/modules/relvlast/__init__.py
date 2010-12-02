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


@mod.route('/<entry:entry>/')
def entry(entry):
    return render_response('relvlast/entry.html', {
        'entry': db['entries'][entry],
        'languages': db['languages'],
    })


@mod.route('/<entry:entry>/revisions/<lang:language>/')
def revisions(entry, language):
    entry = db['entries'][entry]
    return render_response('relvlast/revisions.html', {
        'entry': entry,
        'language': language,
        'history': entry.history(language),
    })
