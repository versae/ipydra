# IPydra
# Template for ipython notebook config

c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.enable_mathjax = True
c.NotebookApp.open_browser = False
#c.NotebookApp.certfile = u'{{ ip_dir }}/security/ssl_{{ username }}.pem'
c.NotebookApp.ipython_dir = u'{{ ip_dir }}'

#from IPython.lib import passwd
#with open('{{ ip_dir }}/pass','r') as fp:
#    p = fp.read().strip()
#c.NotebookApp.password = unicode(passwd(p))

#c.IPKernelApp.pylab = 'inline'
c.NotebookManager.notebook_dir = u'{{ nb_dir }}'
