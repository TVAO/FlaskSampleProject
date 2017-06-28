
# Manage database setup and run server (admin interface)
""""
    How to run app:
    Set environment variable:
        export THERMOS_ENV=dev
    Run server:
        python manage.py runserver
    Toolbar is loaded and debug set
"""

#! /usr/bin/env python

import os

from thermos import create_app, db

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# Check environment variable or default development
app = create_app(os.getenv('THERMOS_ENV') or 'dev')
manager = Manager(app)


migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
