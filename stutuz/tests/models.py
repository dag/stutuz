#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from stutuz.tests import TestBase
from stutuz.models import Account, Users, History, Revision
from stutuz.models import Definition, Root


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
        """Histories keep logs of Revisions with quick access to the newest"""

        history = History()
        account = Account(username='admin')

        first = history.revise((1, 2, 3), account, 'First!')

        self.assert_is(history.newest, first)
        self.assert_is(history.newest, history[first.timestamp])
        self.assert_tuple_equal(history.newest.object, (1, 2, 3))
        self.assert_is(history.newest.author, account)
        self.assert_equal(history.newest.comment, 'First!')

        second = history.revise((3, 2, 1), account, 'Reversed sequence')

        self.assert_is(history.newest, second)
        self.assert_tuple_equal(history.newest.object, (3, 2, 1))
        self.assert_equal(history.newest.comment, 'Reversed sequence')

        for revision in history.itervalues():
            self.assert_is_instance(revision, Revision)

    def test_entries(self):
        """Entries behave properly"""

        admin = Account(username='admin')

        donri = Root(defining='donri', affixes=['dor', "do'i"])
        donri.history('en').revise(
            Definition(
                definition='x₁ is the daytime of day x₂ at location x₃.',
                notes='See also {nicte}, {djedi}, {tcika}.'),
            admin)

        self.assert_sequence_equal(donri.affixes, ['dor', "do'i"])

        self.assert_equal(donri.history('en').newest.object.definition,
                          'x₁ is the daytime of day x₂ at location x₃.')

        self.assert_equal(donri.history('en').newest.object.notes,
                          'See also {nicte}, {djedi}, {tcika}.')

        self.assert_equal(Root().type, 'gismu')
        self.assert_equal(Root(experimental=True).type, 'experimental gismu')
