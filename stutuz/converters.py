#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from werkzeug.routing import BaseConverter, ValidationError

from stutuz.schemata import Locale, Entry


def schematic_converter(schema):
    """Create a Werkzeug converter from a flaskland schema."""

    class Converter(BaseConverter):

        def to_python(self, value):
            value = schema(value)
            if not value.validate():
                raise ValidationError
            return value.value

        def to_url(self, value):
            return schema(value).u

    return Converter


converters = {
    'lang': schematic_converter(Locale),
    'entry': schematic_converter(Entry),
}
