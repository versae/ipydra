from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipydra.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

ROOT_DIR = '/home/ubuntu/repos/ipydra/data/'
NB_URL = 'https://pycon.unata.com'

from login import bp as bp_login
app.register_blueprint(bp_login)

from admin import bp as bp_admin
app.register_blueprint(bp_admin, url_prefix='/admin')
