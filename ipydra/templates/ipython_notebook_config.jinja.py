# IPydra
# Template for ipython notebook config

c = get_config()
c.NotebookApp.certfile = '/home/ubuntu/repos/mycert.pem'
c.NotebookApp.ip = '*'
c.NotebookApp.enable_mathjax = True
c.NotebookApp.open_browser = False
#c.NotebookApp.certfile = u'{{ ip_dir }}/security/ssl_{{ username }}.pem'
c.NotebookApp.ipython_dir = u'{{ ip_dir }}'

#from IPython.lib import passwd
#with open('{{ ip_dir }}/pass','r') as fp:
#    p = fp.read().strip()
c.NotebookApp.password = 'sha1:5f15fe0cf97a:bcb54ba5adfbec8b871c9d747a908c539298e9bc'

#c.IPKernelApp.pylab = 'inline'
c.NotebookManager.notebook_dir = u'{{ nb_dir }}'
