#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flatland.validation import Validator

from stutuz.extensions import db


class IsLanguageCode(Validator):

    invalid_length = 'Language code must be exactly three letters.'

    invalid_code = 'Invalid language code.'

    def validate(self, element, state):
        if len(element.value) != 3:
            return self.note_error(element, state, 'invalid_length')
        with db() as root:
            if not element.value in root['languages']:
                return self.note_error(element, state, 'invalid_code')
        return True
