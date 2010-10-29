#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from stutuz.tests import TestBase
from stutuz.extensions import db


class Converters(TestBase):

    def test_lang(self):
        """The lang converter matches known language codes"""

        @self.app.route('/_test/<lang:code>')
        def lang_code(code):
            return db['languages'][code]

        response = self.client.get('/_test/en')
        self.assert_404(response)

        response = self.client.get('/_test/eng')
        self.assert_equal(response.data, 'English')
