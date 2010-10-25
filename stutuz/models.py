#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from UserDict import IterableUserDict

from werkzeug import generate_password_hash, check_password_hash
from flaskext.zodb import Model, List, Mapping, Timestamp


class Account(Model):
    """A user account."""

    #: A unique identifier for this account.
    username = None

    password_hash = None

    @property
    def password(self):
        """The account password, automatically hashed with a salt."""
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password):
        """Check if a password is valid for this account.

        :rtype: :class:`bool`

        """
        return check_password_hash(self.password, password)


class Users(Model, IterableUserDict):
    """Collection of user accounts, acts like a :class:`dict`."""

    accounts = Mapping

    @property
    def data(self):
        return self.accounts

    def new(self, username, password):
        """Create a new account.

        :raises: :class:`ValueError`, if the username is taken.
        :rtype: :class:`Account`

        """
        if username in self.accounts:
            raise ValueError('username taken')
        account = Account(username=username, password=password)
        self.accounts[username] = account
        return account

    def authenticate(self, username, password):
        """Authenticate a user against the accounts password.

        :raises: :class:`ValueError`, if the username does not exist.
        :rtype: :class:`bool`

        """
        if username in self.accounts:
            return self.accounts[username].authenticate(password)
        raise ValueError('no such username')


class History(Model):

    revisions = List
    active = None

    def add(self, revision):
        self.revisions.append(revision)
        self.active = revision


class Revision(Model):

    author = None
    comment = None
    timestamp = Timestamp
    object = None
