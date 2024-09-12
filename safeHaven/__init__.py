print(" * Loading Safe Haven...")
import os
from datetime import datetime as d
from functools import wraps
from flask import request, render_template, session, redirect, url_for
from __init__ import app

from interlink.toolkit import site_map

whitelist = os.environ.get('whitelist')
blacklist = os.environ.get('blacklist')

def honeypot(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if session == {}:
      ip = request.remote_addr
      for b in blacklist:
        if ip in blacklist:
          print(" *", str(d.now()) + ' -->', "This IP is blacklisted:", ip)
          print(" *", str(d.now()) + ' -->', "This IP is blacklisted:", ip, file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
          return redirect(url_for('templeton.loginRequired'))
    return f(*args, **kwargs)
  return decorated_function
    
def backdoor(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if session == {}:
      ip = request.remote_addr
      for w in whitelist:
        if ip in whitelist:
          session['yourballslooklikemine'] = ip
    return f(*args, **kwargs)
  return decorated_function

def login(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if session == {}:
      ip = request.remote_addr
      print(" * [USER]", str(d.now()) + ' -->', ip, "directed to login")
      print(" * [USER]", str(d.now()) + ' -->', ip, "directed to login", file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
      return redirect(url_for('templeton.secure_login'))
    return f(*args, **kwargs)
  return decorated_function
   