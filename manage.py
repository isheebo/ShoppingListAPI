import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.models import *

app = create_app(os.getenv('APP_SETTINGS', 'development'))

manager = Manager(app)

migrate = Migrate(app, db)

# Add migrations commands to the manager
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
