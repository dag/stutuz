#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import Module, request, jsonify

from stutuz.extensions import db


mod = Module(__name__)


@mod.route('/entry/<id>')
def entry(id):
    entry = db['entries'][id]
    data = dict(id=entry.id, type=entry.type)
    if hasattr(entry, 'affixes'):
        data['affixes'] = [affix.encode('utf-8') for affix in entry.affixes]
    language = request.args.get('translation')
    if language:
        definition = entry.history(language).newest.object
        data['definition'] = definition.definition
        data['notes'] = definition.notes
    return jsonify(data)
