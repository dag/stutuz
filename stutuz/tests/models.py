#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from stutuz.tests import TestBase
from stutuz.models import Account, Users, History, Revision


class Models(TestBase):

    def test_account(self):
        """Accounts store passwords hashed and authenticates"""

        account = Account(username='admin', password='mipri')
        self.assert_not_equal(account.password, 'mipri')
        self.assert_true(account.authenticate('mipri'))
        self.assert_false(account.authenticate('toldra'))

        account.password = 'cnino'
        self.assert_not_equal(account.password, 'cnino')
        self.assert_false(account.authenticate('mipri'))
        self.assert_true(account.authenticate('cnino'))

    def test_users(self):
        """Users have unique usernames, authenticates by username with password
        """

        users = Users()
        admin = users.new('admin', 'mipri')
        guest = users.new('guest', 'vitke')

        self.assert_is(users['admin'], admin)
        self.assert_is(users['guest'], guest)

        self.assert_true(users.authenticate('admin', 'mipri'))
        self.assert_false(users.authenticate('admin', 'toldra'))
        self.assert_true(users.authenticate('guest', 'vitke'))
        self.assert_false(users.authenticate('guest', 'srera'))

        with self.assert_raises(ValueError):
            users.new('admin', 'ckiku')

        with self.assert_raises(ValueError):
            users.new('guest', 'vitke')

        with self.assert_raises(ValueError):
            users.authenticate('noda', 'da')

    def test_history(self):
        """Histories keep lists of Revisions with last as active"""

        history = History()
        account = Account(username='admin')

        first = history.revise((1, 2, 3), account, 'First!')

        self.assert_is(history.active, first)
        self.assert_is(history.active, history[-1])
        self.assert_tuple_equal(history.active.object, (1, 2, 3))
        self.assert_is(history.active.author, account)

        second = history.revise((3, 2, 1), account, 'Reversed sequence')

        self.assert_is(history.active, second)
        self.assert_tuple_equal(history.active.object, (3, 2, 1))

        for revision in history:
            self.assert_is_instance(revision, Revision)
