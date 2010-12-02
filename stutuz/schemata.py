#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flatland.validation import Validator
from babel import localedata
from flatland import String
from werkzeug.routing import BaseConverter, ValidationError

from stutuz.extensions import db


class IsLocale(Validator):

    invalid_locale = 'Invalid locale.'

    def validate(self, element, state):
        if not localedata.exists(element.value):
            return self.note_error(element, state, 'invalid_locale')
        return True


class Locale(String):
    validators = [IsLocale()]


class IsEntry(Validator):

    undefined_entry = 'Undefined entry.'

    def validate(self, element, state):
        with db() as root:
            if element.value not in root['entries']:
                return self.note_error(element, state, 'undefined_entry')
        return True


class Entry(String):
    validators = [IsEntry()]


def schematic_converter(schema):
    """Create a Werkzeug converter from a flatland schema."""

    class Converter(BaseConverter):

        def to_python(self, value):
            value = schema(value)
            if not value.validate():
                raise ValidationError
            return value.value

        def to_url(self, value):
            return schema(value).u

    return Converter


CONVERTERS = {
    'lang': schematic_converter(Locale),
    'entry': schematic_converter(Entry),
}
