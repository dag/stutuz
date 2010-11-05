#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flask import Module, request, Response, jsonify

from stutuz.extensions import db


mod = Module(__name__)


def jsonerror(msg, code):
    return Response(jsonify(error=msg).data,
                    mimetype='application/json',
                    status=code)


@mod.route('/entry/')
def entry():
    if not request.args.get('id'):
        return jsonerror("Missing required argument 'id'.", 400)
    if request.args['id'] not in db['entries']:
        return jsonerror('Undefined entry.', 404)
    if 'language' in request.args and \
       request.args['language'] not in db['languages']:
        return jsonerror('Invalid language code.', 400)

    entry = db['entries'][request.args['id']]
    data = dict(id=entry.id, type=entry.type)
    if hasattr(entry, 'affixes'):
        data['affixes'] = [affix.encode('utf-8') for affix in entry.affixes]
    if hasattr(entry, 'class_'):
        data['class'] = entry.class_

    language = request.args.get('language')
    if entry.history(language):
        definition = entry.history(language).newest.object
        data['definition'] = definition.definition
        data['notes'] = definition.notes
    return jsonify(data)
