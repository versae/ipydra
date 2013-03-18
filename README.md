ipydra
======

Web interface for spawning IPython Notebook servers. Includes an admin interface for listing spawned notebooks.

Used in PyCon 2013 tutorial: https://us.pycon.org/2013/schedule/presentation/28/

dependencies
============
* Flask 0.9
* Flask-SQLAlchemy 0.16
* Flask-WTF 0.12
* Jinja2 2.6
* WTForms 1.0.3
* IPython 0.13.1
* PyZMQ 2.2.0.1
* Tornado 2.4.1

usage
=====

1. copy the ipydra.cfg.default to ipydra.cfg and configure

2. create the db file
  
  ```python
  from ipydra import db, create_app
  db.create_all(app=create_app())
  ```

3. run the development server
  ```python
  python ipydra/runserver.py
  ```

  or make an wsgi file and server it from apache
  ```python
  """ example wsgi file with virtualenv"""
  activate_this = '/home/ubuntu/repos/venv/bin/activate_this.py'
  execfile(activate_this, dict(__file__=activate_this))

  import site
  site.addsitedir('/home/ubuntu/repos/ipydra')

  from ipydra import create_app
  application = create_app()
  ```

notes
=====

* Flask development server will fail to restart if child notebook servers are still running. Not sure if there's a fix for this, but it doesn't happen with apache.

credits
=======

Author: Zach Howard (https://github.com/zhwrd)

Thanks to ipython-hydra (https://github.com/cni/ipython-hydra) for inspiration.
