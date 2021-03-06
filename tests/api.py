#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from attest import Assert as var
from flask import json

from tests.tools import flask_tests
from stutuz.extensions import db
from stutuz.models import Root, Definition


suite = flask_tests()


@suite.context
def setup():
    donri = Root(id='donri', affixes=['dor', "do'i"])
    donri.history('en').revise(object=Definition(
        definition='x1 is the daytime...',
        notes='See also {nicte}...'
    ))

    with db() as root:
        root['entries']['donri'] = donri

    yield


@suite.test
def entry(client):
    """API exposes entries"""

    response = client.get('/api/1/entry/?id=donri')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert var(json.loads(response.data.obj)) == {
        'id': 'donri',
        'type': 'gismu',
        'affixes': ['dor', "do'i"]
    }

    response = client.get('/api/1/entry/?id=donri&locale=en')
    assert response.status_code == 200
    assert var(json.loads(response.data.obj)) == {
        'id': 'donri',
        'type': 'gismu',
        'affixes': ['dor', "do'i"],
        'definition': 'x1 is the daytime...',
        'notes': 'See also {nicte}...'
    }

    response = client.get('/api/1/entry/')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert 'error' in var(json.loads(response.data.obj))

    response = client.get('/api/1/entry/?id=undef')
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    assert 'error' in var(json.loads(response.data.obj))

    response = client.get('/api/1/entry/?id=donri&locale=zzz')
    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert 'error' in var(json.loads(response.data.obj))
