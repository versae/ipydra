from flask import Flask
from flask.ext import shelve

app = Flask(__name__)
app.debug = True

app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

ROOT_DIR = '/home/ubuntu/repos/ipydra/data/'
NB_URL = 'http://54.235.166.187'

from login import bp as bp_login
app.register_blueprint(bp_login)

from admin import bp as bp_admin
app.register_blueprint(bp_admin, url_prefix='/admin')
