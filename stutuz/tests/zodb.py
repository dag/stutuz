#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from uuid import UUID

from flaskext.zodb import (Model, List, Mapping, BTree,
                           Timestamp, UUID4, current_db,
                           PersistentList, PersistentMapping, OOBTree)

from stutuz.tests import TestBase
from stutuz.extensions import db


class TestModel(Model):

    sequence = List
    mapping = Mapping
    btree = BTree
    timestamp = Timestamp
    id = UUID4
    something_else = None


class ZODB(TestBase):

    def test_model_attributes(self):
        """Model instantiates factories when Model instantiated"""

        instance = TestModel()
        self.assert_is_instance(instance.sequence, PersistentList)
        self.assert_is_instance(instance.mapping, PersistentMapping)
        self.assert_is_instance(instance.btree, OOBTree)
        self.assert_is_instance(instance.timestamp, datetime)
        self.assert_is_instance(instance.id, UUID)
        self.assert_is(instance.something_else, None)

    def test_model_kwargs(self):
        """Model init sets attributes with kwargs"""

        instance = TestModel(sequence=(1, 2, 3), mapping={'foo': 'bar'},
                             btree={'bar': 'foo'})
        self.assert_is_instance(instance.sequence, PersistentList)
        self.assert_is_instance(instance.mapping, PersistentMapping)
        self.assert_is_instance(instance.btree, OOBTree)
        self.assert_sequence_equal(instance.sequence, (1, 2, 3))
        self.assert_is(instance.something_else, None)

        instance = TestModel(other='foo', something_else=123)
        self.assert_equal(instance.other, 'foo')
        self.assert_equal(instance.something_else, 123)

    def test_read(self):
        """Views can read from the database"""

        with db() as root:
            root['_test'] = 'Victory!'

        @self.app.route('/_test/')
        def read_value():
            return db['_test']

        rv = self.client.get('/_test/')
        self.assert_equal(rv.data, 'Victory!')

    def test_write(self):
        """Views can write to the database"""

        @self.app.route('/_test/<value>')
        def write_value(value):
            db['_test'] = value

        self.client.get('/_test/Written!')

        with db() as root:
            self.assert_equal(root['_test'], 'Written!')

    def test_local_proxy(self):
        """current_db proxies to the ZODB instance"""

        self.assert_is(current_db.app, self.app)
        self.assert_equal(self.app.extensions['zodb'], current_db)
        self.assert_is(self.app.extensions['zodb'],
                       current_db._get_current_object())