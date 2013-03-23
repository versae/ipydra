ipydra
======

Web interface for spawning IPython Notebook servers. Includes an admin interface for listing spawned notebooks.

Used in PyCon 2013 tutorial: https://us.pycon.org/2013/schedule/presentation/28/

usage
=====

1. install dependencies

  ```
  pip install -r requirements.txt
  ```

2. copy the ipydra.cfg.default to ipydra.cfg and configure

3. create the db file

  ```python
  from ipydra import db, create_app
  db.create_all(app=create_app())
  ```

4. run the development server
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

* Exposing IPython notebooks listening on all IP addresses is highly insecure. I highly recommend running this in a dedicated VM or sandboxed environment.

credits
=======

Author: Zach Howard (https://github.com/zhwrd)

Thanks to ipython-hydra (https://github.com/cni/ipython-hydra) for inspiration.
