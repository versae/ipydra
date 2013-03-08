from flask import Blueprint
from flask import render_template

from ipydra import models
from ipydra import NB_URL

bp = Blueprint('admin', __name__)

@bp.route('/')
def listing():
    return render_template('admin.jinja.html',
                           NB_URL=NB_URL,
                           users=models.User.query.all())
