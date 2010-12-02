#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import print_function
from __future__ import unicode_literals

import os

from flask import current_app
from flaskext.script import Manager, Server

from stutuz import create_app


class Serve(Server):
    description = 'Run the development server.'


manager = Manager(create_app, with_default_commands=False)
manager.add_option('-c', '--config', dest='config',
                   default='stutuz.configs.development')
manager.add_command('serve', Serve())


@manager.option('-r', '--reporter', metavar='NAME')
@manager.option('args', nargs='*')
def test(reporter, args):
    """Run all stutuz tests."""
    from attest import get_reporter_by_name
    from stutuz.tests import all
    all.run(get_reporter_by_name(reporter)(*args))


@manager.command
def shell():
    """Interactive stutuz console."""
    from inspect import cleandoc
    from stutuz import db, models

    banner = '''\
        Interactive stutuz console.

        Useful names:

          app     Flask application for stutuz
          db      The database instance
          models  Namespace for all models
        '''

    banner = cleandoc(banner)
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
def import_xml(file, locale):
    """Import data from a jbovlaste XML export."""
    from stutuz import db
    from stutuz.models import Definition, Root, Compound, Particle, Loan
    from stutuz.utils.tex import Tex
    import xml.etree.cElementTree as etree

    with db() as root:
        doc = etree.parse(file)
        for element in doc.getiterator('valsi'):
            id = element.get('word').decode('utf-8')

            if id in root['entries']:
                entry = root['entries'][id]

            else:
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

                entry.id = id
                root['entries'][entry.id] = entry

            definition = Definition()
            for subelement in element:
                text = subelement.text.decode('utf-8')
                case = lambda x: subelement.tag == x

                if case('definition'):
                    definition.definition = Tex(text)
                elif case('notes'):
                    definition.notes = Tex(text)
                elif case('rafsi'):
                    entry.affixes.append(text)
                elif case('selmaho'):
                    entry.class_ = text

            entry.history(locale).revise(definition,
                                         comment='Imported from XML.')

@manager.command
def dump_localedata(locale):
    """Use a Babel locale as base for a new custom one."""
    from babel import localedata
    import pickle
    from pprint import pprint
    with open(localedata._dirname + '/' + locale + '.dat') as data:
        pprint(pickle.load(data))


@manager.command
def install_localedata():
    """Install the custom locales shipped with stutuz."""
    from stutuz.localedata import jbo
    from babel import localedata
    import pickle
    with open(localedata._dirname + '/jbo.dat', 'w') as data:
        pickle.dump(jbo.DATA, data)


@manager.command
def extract_translations():
    """Extract translatable strings."""
    root = current_app.root_path
    os.system('''
        cd {root}
        pybabel extract -F babel.cfg -o messages.pot .
    '''.format(root=root))


@manager.command
def new_translations(locale):
    """Set up a new locale for translations."""
    root = current_app.root_path
    os.system('''
        cd {root}
        pybabel init -i messages.pot -d translations -l {locale}
    '''.format(root=root, locale=locale))


@manager.command
def compile_translations():
    """Compile translated strings."""
    root = current_app.root_path
    os.system('''
        cd {root}
        pybabel compile -d translations
    '''.format(root=root))


@manager.command
def update_translations():
    """Merge existing translations and new strings."""
    root = current_app.root_path
    os.system('''
        cd {root}
        pybabel update -i messages.pot -d translations
    '''.format(root=root))


def main():
    manager.run()


if __name__ == '__main__':
    main()
