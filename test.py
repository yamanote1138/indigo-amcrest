#! /usr/bin/env python

import httplib, urllib2

def xmitToCamera(cgiPath, params):

  host = '192.168.1.13'

  url = 'http://%s/cgi-bin/%s.cgi?' % (host, cgiPath)

  for param in params:
    url = url + '&%s=%s' % (param, params[param])

  print(u"url xmitted: "+url)

  realm = 'Login to AMC0173D67671799E7'
  username = 'admin'
  password = '1ts4tr4p!'

  pwd_mgr = urllib2.HTTPPasswordMgr()
  pwd_mgr.add_password(realm, url, username, password)
  opener = urllib2.build_opener()
  opener.add_handler(urllib2.HTTPDigestAuthHandler(pwd_mgr))
  req = urllib2.Request(url)
  obj = urllib2.urlopen(req)
  print obj.read()

# move camera to preset position
def goToPreset():
  print(u"goToPreset called")
  preset = '1'
  xmitToCamera("ptz", {'action':'start','channel':'0','code':'GotoPreset','arg1':'0','arg2':'1','arg3':'0','arg4':'0'})

goToPreset()