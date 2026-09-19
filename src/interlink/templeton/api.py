import os
from flask import Blueprint
from interlink.formulator import Generator
from interlink.safeHaven import backdoor, login, honeypot
from interlink.toolkit import site_map, DB
from interlink.templeton.decorator import templetonWrapper

templates = os.path.dirname(__file__) + '/templates/'
static = os.path.dirname(__file__) + '/static/'
interlinkAPI = Blueprint('interlinkAPI', __name__, url_prefix='/')
baseURL='/interlink/v1'

@interlinkAPI.route(baseURL)
def interlinkData():
  '''interlink.templeton.api.interlinkData(): /interlink/v1'''
  from interlink import dataCard
  return dataCard['apiData']

@interlinkAPI.route(baseURL + '/getTables/<db>')
@backdoor
@login
@honeypot
def getTables(db):
  '''interlink.templeton.api.getTables(db): /interlink/v1/getTables/{db}'''
  tables = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
  return {'db': db, 'tables': tables}

@interlinkAPI.route(baseURL + '/getTableData/<db>/<table>')
@backdoor
@login
@honeypot
def tableData(db, table):
  '''interlink.templeton.api.getTableData(db): /interlink/v1/getTableData/{db}/{table}'''
  tableData = DB(db, 'DB_USER', 'DB_PASS').getTableData(table)
  columnData = DB(db, 'DB_USER', 'DB_PASS').getColumnData(table)
  keyData = DB(db, 'DB_USER', 'DB_PASS').getKeyData(table)
  description = DB(db, 'DB_USER', 'DB_PASS').getDescription(table)
  getEnumeration = DB(db, 'DB_USER', 'DB_PASS').getEnumData(table)
  getLookup = DB(db, 'DB_USER', 'DB_PASS').getLookupData(table)
  return {'db': db, 'tableData': tableData, 'columnData': columnData, 'keyData': keyData, 'description': description, 'enumeration': getEnumeration, 'lookupTable': getLookup}