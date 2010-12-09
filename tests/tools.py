#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from attest import Tests, Assert, assert_
from lxml import etree

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


def assert_xml(response, xpath):
    """An XPath query on a response returns a True-like result."""
    doc = etree.fromstringlist(response.obj.data)
    assert_(doc.xpath(xpath),
        "XPath {0!r} didn't match:\n{1}".format(xpath, response.obj.data))
