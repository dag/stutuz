#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

from flaskext.script import Manager

from stutuz import create_app


manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config',
                   default='stutuz.configs.development')


@manager.command
def shell():
    """Interactive stutuz console."""
    from flask import current_app
    from stutuz import db, models

    banner = \
"""Interactive stutuz console.

Useful names:

  app     Flask application for stutuz
  db      The database instance
  models  Namespace for all models
"""

    try:
        current_app.preprocess_request()
        context = dict(app=current_app, db=db, models=models)

        try:
            import bpython
        except ImportError:
            import code
            code.interact(banner, local=context)
        else:
            bpython.embed(context, ['-i'], banner)
    finally:
        current_app.process_response(current_app.response_class())


@manager.command
def import_xml(xml, language):
    from stutuz import db
    from stutuz.models import Definition, Root, Compound, Particle, Loan
    import xml.etree.cElementTree as etree

    with db() as root:
        doc = etree.parse(xml)
        for element in doc.getiterator('valsi'):
            case = lambda x: element.get('type') == x

            if case('gismu'):
                entry = Root()
            elif case('lujvo'):
                entry = Compound()
            elif case('cmavo'):
                entry = Particle()
            elif case("fu'ivla"):
                entry = Loan()
            elif case('experimental gismu'):
                entry = Root(experimental=True)
            elif case('experimental cmavo'):
                entry = Particle(experimental=True)
            else:
                continue

            definition = Definition()
            for subelement in element:
                text = subelement.text.decode('utf-8')
                case = lambda x: subelement.tag == x

                if case('definition'):
                    definition.definition = text
                elif case('notes'):
                    definition.notes = text
                elif case('rafsi'):
                    entry.affixes.append(text)
                elif case('selmaho'):
                    entry.class_ = text

            entry.defining = element.get('word').decode('utf-8')
            entry.history(language).revise(definition,
                                           comment='Imported from XML.')

            root['entries'][entry.defining] = entry


@manager.command
def import_language_codes():
    from urllib2 import urlopen
    from contextlib import closing
    from stutuz import db

    url = 'http://www.sil.org/iso639-3/iso-639-3_20100707.tab'
    with closing(urlopen(url)) as data:
        with db() as root:
            for num, line in enumerate(data):
                if num != 0:
                    code, _, _, _, _, _, name, _ = line.split('\t')
                    root['languages'][code] = name


def main():
    manager.run()


if __name__ == '__main__':
    main()
