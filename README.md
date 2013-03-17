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

notes
=====

* Flask development server will fail to restart if child notebook servers are still running. Not sure if there's a fix for this, but it doesn't happen with apache.

credits
=======

Author: Zach Howard (https://github.com/zhwrd)

Thanks to ipython-hydra (https://github.com/cni/ipython-hydra) for inspiration.
