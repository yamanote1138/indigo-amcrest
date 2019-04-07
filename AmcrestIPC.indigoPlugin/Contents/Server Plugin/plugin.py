#! /usr/bin/env python

import sys
sys.path.append('dependencies')

import requests, time
from requests.auth import HTTPDigestAuth

class Plugin(indigo.PluginBase):

  def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.debug = False

  def __del__(self):
    indigo.PluginBase.__del__(self)

  def startup(self):
    self.logger.debug(u"startup called")

  def shutdown(self):
    self.logger.debug(u"shutdown called")

  def toggleDebugging(self):
    self.debug = not self.debug

  def xmitToCamera(self, cgiPath, params, dev):

    if cgiPath is None: return self.logger.error("no cgi path defined")

    url = 'http://%s/cgi-bin/%s.cgi' % (dev.pluginProps['hostname'], cgiPath)
    req = requests.get(url, params=params, auth=HTTPDigestAuth(dev.pluginProps['username'], dev.pluginProps['password']))

    self.logger.debug(u"url xmitted: "+req.url)

    return req

  # move camera to preset position
  def goToPreset(self, pluginAction, dev):

    self.logger.debug(u"goToPreset called")
    if dev is None: return self.logger.error(u"no device defined")

    preset = pluginAction.props['preset']
    if preset is None: return self.logger.error(u"no preset defined")

    params = (
      ('action','start'),
      ('channel',0),
      ('code','GotoPreset'),
      ('arg1',0),
      ('arg2',preset),
      ('arg3',0),
      ('arg4',0)
    )
    self.xmitToCamera("ptz", params, dev)

  def snap(self, pluginAction, dev):
    self.logger.debug(u"snap called")
    if dev is None: return self.logger.error(u"no device defined")
    resp = self.xmitToCamera('snapshot', {}, dev)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    snappath = "%s/%s_%s.jpg" % (dev.pluginProps['basepath'], dev.name, timestr)
    f = open(snappath, 'w')
    f.write(resp.content)
    f.close()

    dev.updateStateOnServer('lastsnap', value=snappath)
