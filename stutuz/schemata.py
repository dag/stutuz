#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flatland import String

from stutuz.validators import IsLanguageCode, IsEntry


class LanguageCode(String):
    validators = [IsLanguageCode()]


class Entry(String):
    validators = [IsEntry()]
