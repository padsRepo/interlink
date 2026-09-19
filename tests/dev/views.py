from interlink import Generator, Tempulation, tempulator, templetonBP, url_not_found, internal_error, honeypot, backdoor, login, DB, site_map, wrapper
from flask import Flask, Blueprint, render_template, url_for, request

viewsBP = Blueprint('/', __name__, url_prefix='/')

@viewsBP.route('/')
@honeypot
@backdoor
def index():
  #catalog = Generator('accounting', 'DB_USER', 'DB_PASS').generateQuery('vProductionWork', 'snid')
  catalog = "NOCATALOG"
  return wrapper('index.html', catalog=catalog)

@viewsBP.route('/about')
@honeypot
@backdoor
def about():
  return wrapper('about.html')

@viewsBP.route('/copyright')
@honeypot
@backdoor
def copyright():
  return wrapper('copyright.html')
