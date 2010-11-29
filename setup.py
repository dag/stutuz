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

    entry_points={
        'console_scripts': [
            'stutuzctl = stutuz.manage:main',
        ],
    },

    install_requires=[
        'Flask>=0.6',
        'Flask-Genshi>=0.5.1',
        'Flask-Script>=0.3.1',
        'Flask-Babel>=0.6',
        'ZODB3>=3.10.1',
        'Logbook>=0.3',
        'flatland==dev',
        'Attest>=0.3',
        'lxml>=2.2.8',
    ],

    test_loader='attest:Loader',
    test_suite=b'stutuz.tests.all',

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
