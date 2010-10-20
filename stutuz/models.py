#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from werkzeug import generate_password_hash, check_password_hash
from flaskext.zodb import Model, List, Mapping, Timestamp


class Account(Model):

    username = None
    password_hash = None

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self.password, password)


class Users(Model):

    accounts = Mapping

    def new(self, username, password):
        if username in self.accounts:
            raise ValueError('username taken')
        account = Account(username=username, password=password)
        self.accounts[username] = account
        return account

    def authenticate(self, username, password):
        return self.accounts[username].authenticate(password)


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
