import os
import os.path
import sh
import subprocess

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask.ext.shelve import get_shelve

bp = Blueprint('admin', __name__)

@bp.route('/')
def listing():
    from ipydra import NB_URL
    db = get_shelve('r')

    notebooks = dict()
    for key, value in db.get('users', dict()).iteritems():
        notebooks[key] = value

    return render_template('admin.jinja.html',
                           NB_URL=NB_URL,
                           notebooks=notebooks)
