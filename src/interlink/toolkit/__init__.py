'''
This is the Toolkit Module. It contains classes and functions that are reuseable across the entire library.

Classes:  
  DB: Database Connection  

Functions:  
  site_map: Object method used to query database  
  get_script_path: path  
'''

import os
import sys
from flask import url_for
from .db import DB

def get_script_path():
  '''Get the directory path of the project'''
  return os.path.dirname(os.path.realpath(sys.argv[0]))

def has_no_empty_params(rule):
  defaults = rule.defaults if rule.defaults is not None else ()
  arguments = rule.arguments if rule.arguments is not None else ()
  return len(defaults) >= len(arguments)

def site_map():
  '''Generate a URL for each view that does not have a GET or POST method.'''
  from __init__ import app
  links = []
  for rule in app.url_map.iter_rules():
  # Filter out rules we can't navigate to in a browser
  # and rules that require parameters
    if "GET" in rule.methods and has_no_empty_params(rule):
      url = url_for(rule.endpoint, **(rule.defaults or {}))
      links.append((url, rule.endpoint))
  # links is now a list of url, endpoint tuples
  return links


