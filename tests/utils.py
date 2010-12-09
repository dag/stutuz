#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from attest import Tests, Assert as var
from flask import Markup

from stutuz.utils.tex import Tex


suite = Tests()


@suite.test
def tex():
    text = '$x_{1}$ is not $x_2$'
    html = 'x<sub>1</sub> is not x<sub>2</sub>'
    assert var(unicode(Tex(text))) == text
    assert var(unicode(Markup(Tex(text)))) == html
