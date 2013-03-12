from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
    db.init_app(app)
    bcrypt.init_app(app)

    from login import bp as bp_login
    app.register_blueprint(bp_login)

    from admin import bp as bp_admin
    app.register_blueprint(bp_admin, url_prefix='/admin')

    return app

ROOT_DIR = '/home/ubuntu/repos/ipydra/data/'
NB_URL = 'http://pycon.unata.com'
