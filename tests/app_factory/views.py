from interlink import Generator, Tempulation, tempulator, templetonBP, url_not_found, internal_error, honeypot, backdoor, login, DB, site_map, wrapper
from flask import Flask, Blueprint, render_template, url_for, request
import os

viewsBP = Blueprint('/', __name__, url_prefix='/')

@viewsBP.route('/')
@honeypot
@backdoor
def index():
  #catalog = Generator('accounting', 'DB_USER', 'DB_PASS').generateQuery('vProductionWork', 'snid')
  error, catalog, lookupTable = Generator('tFood', 'DB_USER', 'DB_PASS').generateForm('vt')
  return wrapper('index.html', catalog=catalog, error=error, lookupTable=lookupTable)

@viewsBP.route('/theme/')
@honeypot
@backdoor
def preview():
  c = "CAT"
  return wrapper('preview.html', catalog=c)

@templetonBP.route('/report/<db>/<table>')
@honeypot
@backdoor
def me(db, table):
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  colName, colRow, error, title = gen.generateReport(table)
  return wrapper('reports.html', colName=colName, colRow=colRow, error=error, title=title)

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
