#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import Module, request, jsonify
from flaskext.genshi import render_response
from babel import Locale

from stutuz.extensions import db


def wants_json():
    return request.is_xhr or \
           request.accept_mimetypes.best == 'application/json' or \
           'json' in request.args


mod = Module(__name__, 'relvlast')


@mod.route('/<entry:entry>/')
def entry(entry):
    entry = db['entries'][entry]

    if wants_json():
        data = dict(id=entry.id, type=entry.type, translations={})
        if hasattr(entry, 'affixes'):
            data['affixes'] = map(str, entry.affixes)
        for code, history in entry.translations.iteritems():
            data['translations'][code] = str(history.newest.object.definition)
        return jsonify(data)

    return render_response('relvlast/entry.html', dict(entry = entry))


@mod.route('/<entry:entry>/+revisions/<lang:language>/')
def revisions(entry, language):
    entry = db['entries'][entry]
    return render_response('relvlast/revisions.html',
        dict(
            entry = entry,
            language = language,
            history = entry.history(language),
        )
    )


@mod.route('/+export/<lang:locale>/')
def export(locale):
    response = render_response('relvlast/export.xml',
        dict(
            language = Locale(locale).english_name,
            locale = locale,
            entries = (e for e in db['entries'].itervalues()
                         if e.translations.get(locale)),
        )
    )
    response.headers.add('Content-Disposition', 'attachment',
                         filename='.'.join(('jbovlaste', locale, 'xml')))
    return response
