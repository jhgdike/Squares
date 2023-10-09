#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from flask_migrate import Migrate, MigrateCommand

from .app import create_app

# from .ext import db

app = create_app()


# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)


def main():
    app.run()


if __name__ == '__main__':
    main()
