#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from attest import Tests, Assert

from stutuz import create_app


def flask_tests():
    tests = Tests()

    @tests.context
    def request_context():
        app = create_app('stutuz.configs.testing')
        with app.test_request_context():
            app.preprocess_request()
            yield Assert(app.test_client())
            app.process_response(app.response_class())

    return tests
