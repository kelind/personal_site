from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mako import MakoTemplates
from flask.ext.migrate import Migrate, MigrateCommand
#from flask_restless import APIManager
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#api = APIManager(app, flask_sqlalchemy_db=db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

mako = MakoTemplates(app)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/personal.log', 'a', 1 * 1024 * 1024, 5)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    
    app.logger.setLevel(logging.WARNING)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler) 

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.before_request
def _before_request():
    g.user = current_user
