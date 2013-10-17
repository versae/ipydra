import httplib2
import os
import re
import subprocess
import shutil
import time
from urllib import urlencode

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
PROXY_DOMAIN = "127.0.0.1:8888"
PROXY_FORMAT = u"http://%s/%s" % (PROXY_DOMAIN, u"%s")
PROXY_REWRITE_REGEX = re.compile(
    r'((?:src|action|[^_]href|project-url|kernel-url|baseurl)'
    '\s*[=:]\s*["\']?)/',
    re.IGNORECASE
)


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


@bp.route('/proxy/', defaults={'url': ''},
          methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"])
@bp.route('/proxy/<path:url>',
          methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"])
def proxy(url):
    conn = httplib2.Http()
    # optionally provide authentication for server
    #conn.add_credentials('admin','admin-password')
    if request.method == "GET":
        url_ending = "%s?%s" % (url, request.query_string)
        url = PROXY_FORMAT % url_ending
        resp, content = conn.request(url, request.method)
    elif request.method == "POST":
        url = PROXY_FORMAT % url
        data = urlencode(request.data)
        resp, content = conn.request(url, request.method, data)
    else:
        url = PROXY_FORMAT % url
        resp, content = conn.request(url, request.method)
    if content:
        content = PROXY_REWRITE_REGEX.sub(r'\1/proxy/', content)
    if "content-type" in resp:
        mimetype = resp["content-type"].split(";")[0].split(",")[0]
    else:
        mimetype = None
    response = Response(
        content,
        headers=resp,
        mimetype=mimetype
    )
    return response
proxy.provide_automatic_options = False


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
