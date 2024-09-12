import os
import sys
import mysql.connector
from flask import url_for

from __init__ import app

metadata = {
  "version": "0.0.4",
  "createDate": "01-21-2024",
  "updateDate": "09-10-2024",
  "author": "Joe Corso",
  "docs": "https://github.com/padsRepo/interlink/wiki"
}

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def has_no_empty_params(rule):
  defaults = rule.defaults if rule.defaults is not None else ()
  arguments = rule.arguments if rule.arguments is not None else ()
  return len(defaults) >= len(arguments)

def site_map():
  links = []
  for rule in app.url_map.iter_rules():
  # Filter out rules we can't navigate to in a browser
  # and rules that require parameters
    if "GET" in rule.methods and has_no_empty_params(rule):
      url = url_for(rule.endpoint, **(rule.defaults or {}))
      links.append((url, rule.endpoint))
  # links is now a list of url, endpoint tuples
  return links

# TO USE:
# db = DB('ACCOUNTING_DB', 'DB_USER', 'DB_PASS').connect()
# cursor = db.cursor(buffered=True)
# db.close()

class DB:
  def __init__(self, db, user, password):
    self.db = db
    self.user = user
    self.password = password
  def connect(self):
    mydb = mysql.connector.connect(
    host='localhost',
    database=os.environ.get(self.db),
    user=os.environ.get(self.user),
    password=os.environ.get(self.password)
    )
    return mydb
  def close(self):
    db = DB(self.db, self.user, self.password)
    if db is not None:
      db.close()
