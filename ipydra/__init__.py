from flask import Flask
from flask.ext import shelve
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.debug = True

bcrypt = Bcrypt(app)

app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

ROOT_DIR = '/home/ubuntu/repos/ipydra/data/'
NB_URL = 'https://pycon.unata.com'

from login import bp as bp_login
app.register_blueprint(bp_login)

from admin import bp as bp_admin
app.register_blueprint(bp_admin, url_prefix='/admin')
