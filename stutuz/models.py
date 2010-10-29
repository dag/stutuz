#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from werkzeug import generate_password_hash, check_password_hash
from flaskext.zodb import Model, Timestamp, Mapping, List
from flaskext.zodb import PersistentList, PersistentMapping


class Users(PersistentMapping):
    """Collection of user accounts, acts like a :class:`dict`."""

    def new(self, username, password):
        """Create a new account.

        :raises ValueError: For usernames that are already registered.
        :rtype: :class:`Account`

        """
        if username in self:
            raise ValueError('username taken')
        account = Account(username=username, password=password)
        self[username] = account
        return account

    def authenticate(self, username, password):
        """Authenticate a user against the accounts password.

        :raises ValueError: For usernames that are not registered.
        :rtype: :class:`bool`

        """
        if username in self:
            return self[username].authenticate(password)
        raise ValueError('no such username')


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


class History(PersistentList):
    """A sequence of revisions, acts like a :class:`list`."""

    @property
    def active(self):
        """The active revision, i.e. the last added."""
        return self[-1]

    def revise(self, object, author=None, comment=None):
        """Create a new revision and append to the history.

        :rtype: :class:`Revision`

        """
        self.append(Revision(author=author, comment=comment, object=object))
        return self.active


class Revision(Model):
    """Metadata wrapping a version of an object."""

    #: The :class:`Account` that authored this revision.
    author = None

    #: A comment describing the reason for the revision.
    comment = None

    #: An automatic timestamp of when the revision was created.
    timestamp = Timestamp

    #: The wrapped object.
    object = None


class Definition(Model):
    """Definition of an entry in some language."""

    #: The actual definition.
    definition = None

    #: Accompanying notes.
    notes = None


class Entry(Model):
    """Base for dictionary entries."""

    #: The word or sequence of words that this entry defines.
    defining = None

    translations = Mapping

    def history(self, language):
        """Get the history of revisions in a language, create if needed."""
        if language not in self.translations:
            self.translations[language] = History()
        return self.translations[language]

    @property
    def type(self):
        return {
            Root: 'gismu',
            Compound: 'lujvo',
            Particle: 'cmavo',
            Loan: "fu'ivla"
        }[self.__class__]


class AffixesMixin(object):
    """Mixin for words that can have affixes."""

    #: List of affix forms ("rafsi") of this word.
    affixes = List


class ExperimentalMixin(object):
    """Words that can be experimental."""

    #: Whether this word is experimental.
    experimental = False

    @property
    def type(self):
        if self.experimental:
            return 'experimental ' + super(ExperimentalMixin, self).type
        return super(ExperimentalMixin, self).type


class Root(ExperimentalMixin, Entry, AffixesMixin):
    """A root word, aka. "gismu"."""

    #: Map of language codes to words this root is based on.
    etymology = Mapping


class Compound(Entry):
    """Word built with affixes, aka. "lujvo"."""

    #: The metaphor ("tanru") that results in this compound.
    source = None


class Particle(ExperimentalMixin, Entry, AffixesMixin):
    """Grammatical particle, aka. "cmavo"."""

    #: Grammatical class ("selma'o").
    class_ = None


class Loan(Entry, AffixesMixin):
    """Word borrowed from a foreign language, aka. "fu'ivla"."""

    #: The word this loanword is based on.
    base = None

    #: The language code for the language this word was borrowed from.
    origin = None
