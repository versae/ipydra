import os
import os.path
import sh
import subprocess

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from ipydra import models

bp = Blueprint('admin', __name__)

@bp.route('/')
def listing():
    from ipydra import NB_URL
    return render_template('admin.jinja.html',
                           NB_URL=NB_URL,
                           users=models.User.query.all())
