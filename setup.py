#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import sys

from setuptools import setup, find_packages


assert sys.version_info[0:2] in ((2, 6), (2, 7)), \
       'Python 2.6 or 2.7 is required'


setup(
    name='stutuz',
    version='0.1dev',
    description='Prototypical foundation for a Lojban web infrastructure '
                'with a focus on Jbovlaste 2.',

    author='Dag Odenhall',
    author_email='dag.odenhall@gmail.com',
    license='Simplified BSD',
    url='http://github.com/dag/stutuz',

    packages=find_packages(),
    namespace_packages=['flaskext'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Flask>=0.6',
        'Flask-Genshi>=0.4',
        'Flask-Script>=0.3.1',
        'ZODB3>=3.10.0',
    ],

    tests_require=[
        'Flask-Testing>=0.2.4',
    ],

    test_suite='stutuz.tests',

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
