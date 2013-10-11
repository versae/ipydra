import os
import subprocess
import shutil
import time

from flask import Blueprint
from flask import redirect
from flask import request
from flask import Response
from flask import render_template

from ipydra import db
from ipydra import models
from ipydra import DATA_DIR
from ipydra import BASE_URL
from ipydra import INITDATA_DIR
from ipydra.backends import LoginForm


bp = Blueprint('login', __name__)


@bp.route('/', methods=['GET', 'POST'])
def login():
    """ Login view which redirects the user to the spawned servers.
    """
    form = LoginForm(csrf_enabled=False)
    form_is_valid = form.validate_on_submit()
    if form_is_valid:
        username = str(form.username.data)
        users = models.User.query.filter(models.User.username == username)
        user = users.first()
        # create user model if it doesn't exist for the given username
        if not user:
            # get the next server port
            port = 9499 + models.User.query.count() + 1
            # create user
            user = models.User()
            user.username = username
            user.nbserver_port = port
            user = db.session.merge(user)
            db.session.commit()
        # create the user data directory hierarchy
        if not os.path.exists('{0}/{1}'.format(DATA_DIR, username)):
            create_user_dir(username)
        # spawn the notebook server if its not currently running
        if (not user.nbserver_pid or
                not os.path.exists('/proc/{0}'.format(user.nbserver_pid))):
            ip_dir = '{0}/{1}/.ipython'.format(DATA_DIR, username)
            user.nbserver_pid = run_server(ip_dir, user.nbserver_port)
            user = db.session.merge(user)
            db.session.commit()
            # sleep to let server start listening
            time.sleep(1)
        return redirect('{0}:{1}'.format(BASE_URL, user.nbserver_port))
    return render_template('login.jinja.html', form=form,
                           is_valid=form_is_valid)


@bp.route('/proxy/')
def proxy():
    response = Response(None, mimetype='text/plain')
    return response


def run_server(ip_dir, port):
    """ Run a notebook server with a given ipython directory and port.
        Returns a PID.
    """
    pid = subprocess.Popen([
        'ipython',
        'notebook',
        '--profile=nbserver',
        '--NotebookApp.port={0}'.format(port),
        '--NotebookApp.ipython_dir={0}'.format(ip_dir)
    ]).pid
    return pid


def create_user_dir(username):
    """ Create a new user's directory structure.
    """
    user_dir = '{0}/{1}'.format(DATA_DIR, username)
    ip_dir = '{0}/.ipython'.format(user_dir)
    conf_dir = '{0}/profile_nbserver'.format(ip_dir)
    nb_dir = '{0}/notebooks'.format(user_dir)

    os.makedirs(ip_dir)
    os.makedirs(conf_dir)

    # render config
    config = render_template('ipython_notebook_config.jinja.py',
                             username=username,
                             ip_dir=ip_dir,
                             nb_dir=nb_dir)
    config_file = open('{0}/ipython_notebook_config.py'.format(conf_dir), 'w')
    config_file.write(config)
    config_file.close()

    # copy data files over
    if INITDATA_DIR:
        shutil.copytree(INITDATA_DIR, '{0}'.format(nb_dir))
    else:
        os.makedirs(nb_dir)

    # render update_score script
    script = render_template('update_score.jinja.py', username=username)
    script_file = open('{0}/update_score.py'.format(nb_dir), 'w')
    script_file.write(script)
    script_file.close()
