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


def main():
    manager.run()


if __name__ == '__main__':
    main()