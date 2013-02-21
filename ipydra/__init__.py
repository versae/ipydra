from flask import Flask
from flask.ext import shelve

app = Flask(__name__)
app.debug = True

app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

ROOT_DIR = '/home/ubuntu/repos/ipydra/data/'

from frontend import bp as bp_frontend
app.register_blueprint(bp_frontend)
