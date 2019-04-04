#! /usr/bin/env python

import httplib, os, requests, smtplib, sys, urllib2
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from requests.auth import HTTPDigestAuth

class Plugin(indigo.PluginBase):

  def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
    indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
    self.debug = True

  def __del__(self):
    indigo.PluginBase.__del__(self)

  def startup(self):
    self.debugLog(u"startup called")

  def shutdown(self):
    self.debugLog(u"shutdown called")

  def xmitToCamera(self, cgiPath, params, dev):

    if cgiPath is None: return self.debugLog("no path defined")

    url = 'http://%s/cgi-bin/%s.cgi' % (dev.pluginProps['hostname'], cgiPath)
    req = requests.get(url, params=params, auth=HTTPDigestAuth(dev.pluginProps['username'], dev.pluginProps['password']))

    self.debugLog(u"url xmitted: "+req.url)

    return req

  # move camera to preset position
  def goToPreset(self, pluginAction, dev):

    self.debugLog(u"goToPreset called")
    if dev is None: return self.debugLog(u"no device defined")

    preset = pluginAction.props['preset']
    if preset is None: return self.debugLog(u"no preset defined")

    self.xmitToCamera("decoder_control.cgi", {'command': str(self.presets[preset]['go'])}, dev)

  #Enable Infrared LEDs
  def irOn(self, pluginAction, dev):
  
    self.debugLog(u"irOn called")
    if dev is None: 
      return self.debugLog(u"no device defined")
    self.xmitToCamera("decoder_control.cgi", {'command':95}, dev)

  #Disable Infrared LEDs
  def irOff(self, pluginAction, dev):
  
    self.debugLog(u"irOff called")
    if dev is None: 
      return self.debugLog(u"no device defined")
    self.xmitToCamera("decoder_control.cgi", {'command':94}, dev)

  def snap(self, pluginAction, dev):
  
    self.debugLog(u"snap called")
    if dev is None: 
      return self.debugLog(u"no device defined")
    resp = self.xmitToCamera('snapshot.cgi', {}, dev)
    snapimg = resp.read()

    # todo: serialize filename, pass to sendViaEmail
    snappath = "/tmp/snap.jpg"
    f = open(snappath, 'w')
    f.write(snapimg)
    f.close()

    self.sendViaEmail(pluginAction, dev)

  def sendViaEmail(self, pluginAction, dev):
    
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = pluginAction.props['subject']
    msg['From'] = self.pluginPrefs['sender']
    msg['To'] = pluginAction.props['recipient']
    msg.preamble = 'cam snap test'

    # Open the files in binary mode.  Let the MIMEImage class automatically
    # guess the specific image type.
    fp = open('/tmp/snap.jpg', 'rb')
    img = MIMEImage(fp.read(), "jpeg")
    fp.close()
    msg.attach(img)

    s = smtplib.SMTP(self.pluginPrefs['smtphost'],int(self.pluginPrefs['smtpport']))
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(self.pluginPrefs['smtpuser'], self.pluginPrefs['smtppass'])
    s.sendmail(self.pluginPrefs['sender'], pluginAction.props['recipient'], msg.as_string())
    s.quit()
