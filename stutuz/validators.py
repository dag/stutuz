#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flatland.validation import Validator
from babel import localedata

from stutuz.extensions import db


class IsLocale(Validator):

    invalid_locale = 'Invalid locale.'

    def validate(self, element, state):
        if not localedata.exists(element.value):
            return self.note_error(element, state, 'invalid_locale')
        return True


class IsEntry(Validator):

    undefined_entry = 'Undefined entry.'

    def validate(self, element, state):
        with db() as root:
            if element.value not in root['entries']:
                return self.note_error(element, state, 'undefined_entry')
        return True
