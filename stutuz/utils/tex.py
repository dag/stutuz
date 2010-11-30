#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import re


class Tex(object):
    """Wraps a string of TeX such that wrapping it in
    :class:`~flask.Markup` gives a HTML representation, otherwise the
    original string.

    """

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text

    def __repr__(self):
        return 'Tex({0!r})'.format(self.text)

    def __html__(self):
        return _tex_to_html(self.text)


def _tex_to_html(tex):
    tex = re.sub(r'\$(.+?)\$', _sub_math, tex)
    tex = re.sub(r'\\(emph|textbf)\{(.+?)\}', _sub_typography, tex)
    tex = re.sub(r'(?![|>\-])\s\s+(.+)', _sub_lines, tex)
    tex = re.sub(r'inchoative\s\s+(----.+)', _sub_puho, tex)
    return tex


def _sub_math(m):
    t = []
    for x in m.group(1).split('='):
        x = x.replace('{', '').replace('}', '')
        x = x.replace('*', u'×')
        if '_' in x:
            t.append(u'%s<sub>%s</sub>' % tuple(x.split('_')[0:2]))
        elif '^' in x:
            t.append(u'%s<sup>%s</sup>' % tuple(x.split('^')[0:2]))
        else:
            t.append(x)
    return '='.join(t)


def _sub_typography(m):
    if m.group(1) == 'emph':
        return u'<em>%s</em>' % m.group(2)
    elif m.group(1) == 'textbf':
        return u'<strong>%s</strong>' % m.group(2)


def _sub_lines(m):
    format = '\n%s'
    if m.group(1).startswith('|'):
        format = '\n<span style="font-family: monospace">    %s</span>'
    elif m.group(1).startswith('>'):
        format = '\n<span style="font-family: monospace">   %s</span>'
    return format % m.group(1)


def _sub_puho(m):
    format = 'inchoative\n<span style="font-family: monospace">%s</span>'
    return format % m.group(1)
