#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from attest import Tests, Assert

from stutuz.models import Account, Users, History, Revision
from stutuz.models import Definition, Root


suite = Tests()


@suite.test
def account():
    """Accounts store passwords hashed and authenticates"""

    account = Assert(Account(username='admin', password='mipri'))
    assert account.password != 'mipri'
    assert account.authenticate('mipri').is_(True)
    assert account.authenticate('toldra').is_(False)

    account.obj.password = 'cnino'
    assert account.password != 'cnino'
    assert account.authenticate('mipri').is_(False)
    assert account.authenticate('cnino').is_(True)


@suite.test
def users():
    """Users have unique usernames, authenticates by username with password"""

    users = Assert(Users())
    admin = users.new('admin', 'mipri').obj
    guest = users.new('guest', 'vitke').obj

    assert users['admin'].is_(admin)
    assert users['guest'].is_(guest)

    assert users.authenticate('admin', 'mipri').is_(True)
    assert users.authenticate('admin', 'toldra').is_(False)
    assert users.authenticate('guest', 'vitke').is_(True)
    assert users.authenticate('guest', 'srera').is_(False)

    with Assert.raises(ValueError):
        users.new('admin', 'ckiku')

    with Assert.raises(ValueError):
        users.new('guest', 'vitke')

    with Assert.raises(ValueError):
        users.authenticate('noda', 'da')


@suite.test
def history():
    """Histories keep logs of Revisions with quick access to the newest"""

    history = Assert(History())
    account = Account(username='admin')

    first = history.revise((1, 2, 3), account, 'First!').obj

    assert history.newest.is_(first)
    assert history.newest.is_(history[first.timestamp.isoformat()].obj)
    assert history.newest.object == (1, 2, 3)
    assert history.newest.author.is_(account)
    assert history.newest.comment == 'First!'

    second = history.revise((3, 2, 1), account, 'Reversed sequence').obj

    assert history.newest.is_(second)
    assert history.newest.object == (3, 2, 1)
    assert history.newest.comment == 'Reversed sequence'

    for revision in history.values():
        assert revision.__class__.is_(Revision)


@suite.test
def entries():
    """Entries behave properly"""

    admin = Account(username='admin')

    donri = Assert(Root(id='donri', affixes=['dor', "do'i"]))
    donri.history('en').revise(
        Definition(
            definition='x₁ is the daytime of day x₂ at location x₃.',
            notes='See also {nicte}, {djedi}, {tcika}.'),
        admin)

    assert donri.affixes == ['dor', "do'i"]

    assert donri.history('en').newest.object.definition == \
           'x₁ is the daytime of day x₂ at location x₃.'

    assert donri.history('en').newest.object.notes == \
           'See also {nicte}, {djedi}, {tcika}.'

    Assert(Root().type) == 'gismu'
    Assert(Root(experimental=True).type) == 'experimental gismu'
