#! /usr/bin/env python

import sys
sys.path.append('dependencies')

import requests, time
from requests.auth import HTTPDigestAuth

def xmitToCamera(cgiPath, params=None):

  # note: params has to be a sequence of two-valud tuples in order to stay in order
  # unfortunately, Amcrest's API doesn't work if the params aren't in a set order

  host = '192.168.1.11'
  username = 'admin'
  password = 'thr33p10'

  url = 'http://%s/cgi-bin/%s.cgi' % (host, cgiPath)
  return requests.get(url, params=params, auth=HTTPDigestAuth(username, password))

# move camera to preset position
def goToPreset():
  print(u"goToPreset called")
  params = (
    ('action','start'),
    ('channel',0),
    ('code','GotoPreset'),
    ('arg1',0),
    ('arg2',1),
    ('arg3',0),
    ('arg4',0)
  )
  xmitToCamera("ptz", params)

def snap():
  resp = xmitToCamera('snapshot.cgi')

  # todo: serialize filename, pass to sendViaEmail
  timestr = time.strftime("%Y%m%d-%H%M%S")
  snappath = "/tmp/streetwise_"+timestr+".jpg"
  f = open(snappath, 'w')
  f.write(resp.content)
  f.close()

# goToPreset()
snap()