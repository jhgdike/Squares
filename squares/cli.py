#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager as Managers
# from flask_migrate import Migrate, MigrateCommand

from .app import create_app
# from .ext import db

app = create_app('development')
# migrate = Migrate(app, db)

manager = Managers(app)

# manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return {'app': app}


def main():
    manager.run()

if __name__ == '__main__':
    main()
