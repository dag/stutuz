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


@manager.option('-r', '--reporter', metavar='NAME')
@manager.option('args', nargs='*')
def runtests(reporter, args):
    """Run all stutuz tests."""
    from attest import get_reporter_by_name
    from stutuz.tests import all
    all.run(get_reporter_by_name(reporter)(*args))


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
def import_xml(xml, locale):
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

            entry.id = element.get('word').decode('utf-8')
            entry.history(locale).revise(definition,
                                         comment='Imported from XML.')

            root['entries'][entry.id] = entry


def main():
    manager.run()


if __name__ == '__main__':
    main()
