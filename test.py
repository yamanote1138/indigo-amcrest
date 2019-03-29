#! /usr/bin/env python

import requests
from requests.auth import HTTPDigestAuth

def xmitToCamera(cgiPath, params):

  host = '192.168.1.13'
  username = 'admin'
  password = '1ts4tr4p!'

  # url = 'http://%s/cgi-bin/%s.cgi?' % (host, cgiPath)
  # for param in params:
  #   url = url + '&%s=%s' % (param, params[param])

  url = 'http://192.168.1.13/cgi-bin/ptz.cgi?action=start&channel=0&code=GotoPreset&arg1=0&arg2=1&arg3=0&arg4=0'

  print(u"url xmitted: "+url)
  requests.get(url, auth=HTTPDigestAuth(username, password))

# move camera to preset position
def goToPreset():
  print(u"goToPreset called")
  preset = '1'
  xmitToCamera("ptz", {'action':'start','channel':'0','code':'GotoPreset','arg1':'0','arg2':'1','arg3':'0','arg4':'0'})

goToPreset()