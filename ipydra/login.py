import os
import os.path
import sh
import subprocess

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask.ext.shelve import get_shelve
from flask.ext.wtf import Form
from flask.ext.wtf import TextField

bp = Blueprint('frontend', __name__)

class LoginForm(Form):
    username = TextField('Username')

@bp.route('/', methods=['GET', 'POST'])
def nbserver():
    from ipydra import ROOT_DIR
    from ipydra import NB_URL

    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        db = get_shelve('c')
        username = str(form.username.data)
        ip_dir = '{0}/.ipython'.format(ROOT_DIR + username)
        # create user directories if they dont exist
        if not user_exists(username):
            create_user(username)
        # check if user already has a server running
        if username not in db:
            # increment port counter
            if 'count' not in db:
                db['count'] = 9499
            db['count'] += 1
            port = db['count']
            # start server
            pid = run_server(ip_dir, port)
            users = db.get('users', dict())
            users[username] = {'pid': pid, 'port': port}
            db['users'] = users
            # sleep to let the server start and listen
            sh.sleep(1)
        else:
            port = db['users'][username]['port']
        return redirect('{0}:{1}'.format(NB_URL, port))
    return render_template('login.jinja.html', form=form)

def run_server(ip_dir, port):
    """ Run a notebook server with a given ipython directory and port.
        Returns a PID.
    """ 
    pid = subprocess.Popen(['/home/ubuntu/repos/venv/bin/ipython',
                            'notebook',
                            '--profile=nbserver',
                            '--NotebookApp.port={0}'.format(port),
                            '--NotebookApp.ipython_dir={0}'.format(ip_dir)]).pid
    return pid

def user_exists(username):
    """ Check if user exists.
    """
    from ipydra import ROOT_DIR
    return os.path.exists('{0}{1}'.format(ROOT_DIR, username))

def create_user(username):
    """ Create a new user.
    """
    from ipydra import ROOT_DIR

    user_dir = '{0}{1}'.format(ROOT_DIR, username)
    ip_dir = '{0}/.ipython'.format(user_dir)
    log_file = '{0}/log'.format(ip_dir)
    conf_dir = '{0}/profile_nbserver'.format(ip_dir)
    nb_dir = '{0}/notebooks'.format(user_dir)
    data_dir = '{0}/data'.format(user_dir)

    os.makedirs(ip_dir)
    os.makedirs(conf_dir)
    os.makedirs(nb_dir)
    os.makedirs(data_dir)
    sh.touch(log_file)

    # generate ssl cert

    # render config
    config = render_template('ipython_notebook_config.jinja.py',
                             username=username,
                             ip_dir=ip_dir,
                             nb_dir=nb_dir)
    config_file = open('{0}/ipython_notebook_config.py'.format(conf_dir), 'w')
    config_file.write(config)
    config_file.close()

    # clone git repo
    #git_repo = 'git://github.com/UnataInc/ipython-hydra.git'
    #sh.git.clone(git_repo, nb_dir)
