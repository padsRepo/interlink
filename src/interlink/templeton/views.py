import os
from flask import Blueprint, render_template, request
import interlink
from interlink.formulator import Generator
from interlink.safeHaven import backdoor, login, honeypot
from interlink.toolkit import site_map, DB
from interlink.templeton import tempulator
from interlink.templeton.decorator import templetonWrapper

# Interlink data sheet
@templetonWrapper('data.html')
def data():
  '''interlink.templeton.views.data'''
  from interlink import dataCard
  return dataCard['routeData']

@templetonWrapper()
def license():
  pass

# Interlink wiki
def documentation(page = 'index.html'):
  '''interlink.templeton.views.documentation(page)'''
  return render_template('guide/' + page)

# Blog 
@templetonWrapper('blog.html')
def blog(db, table):
  '''interlink.templeton.views.blog(db, table)'''
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  colName, colRow, error, title = gen.generateReport(table)
  return dict(colName=colName, colRow=colRow, error=error, title=title)

# Storefront
@templetonWrapper('store.html')
def store(db, table):
  '''interlink.templeton.views.store(db, table)'''
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  catalog = gen.generateQuery(table)
  title = 'Store'
  return dict(catalog=catalog, title=title)

# Reports
@templetonWrapper('reports.html')
@backdoor
@login
@honeypot
def generateReport(db, table):
  '''interlink.templeton.views.generateReport(db, table)'''
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  colName, colRow, error, title = gen.generateReport(table)
  return dict(colName=colName, colRow=colRow, error=error, title=title)

# Forms
# TODO: Needs to have 'GET' method
# This may not work
@templetonWrapper('forms.html')
@backdoor
@login
@honeypot
def generateForm(db, table):
  '''interlink.templeton.views.generateForm(db, table)'''
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  error, colName, lookupTable = gen.generateForm(table)
  return dict(lookupTable=lookupTable, colName=colName, error=error)

# Admin
@templetonWrapper('admin.html')
@backdoor
@login
@honeypot
def admin(db):
  '''interlink.templeton.views.admin(db)'''
  nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
  return dict(nav=nav, db=db, title=db)
