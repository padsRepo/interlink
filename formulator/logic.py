import os
from flask import request
from interlink.toolkit import DB

def createQuery(db, user, password, table):
  db_conn = DB(db, user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  sql = f'''SELECT * FROM {table};'''
  cursor.execute(sql)
  sql = cursor.fetchall()
  db_conn.close()
  if sql is not None:
    print(" *", table, "Report Read.")
  else:
    sql = " * No", table, "Report"
    print(" * No", table, "Report")
  return sql
 
def createFilter(db, user, password):
  report = None
  if request.method == 'POST':
    padsFilter1 = request.form['filter1']
    padsFilter2 = request.form['filter2']
    if padsFilter1 == "" or padsFilter2 == "":
      return report
    else:
      try:
        db_conn = DB.db_conn(db, user, password)
        cursor = db_conn.cursor(buffered=True)
        report = f'''SELECT {col} FROM {table};'''
        cursor.execute(sql)
        report = cursor.fetchall()
        DB.db_close(db, user, password)
        if report is not None:
          print(" * Filter:", padsFilter2, "Report Read.")
      except:
        report = ' * That is not a report.'
        print(report)
    return report

def createNav(db, user, password):
  schema = os.environ.get(db)
  db_conn = DB(db, user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{schema}'; ''')
  sql = cursor.fetchall()
  db_conn.close()
  return sql

def createReport(db, user, password, table):
  error = f'''{table} Report Does Not Exist'''
  colName = ''
  colRow = ''
  db_conn = DB(db, user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{table}'; ''')
  check_table = cursor.fetchone()
  if check_table is not None:
    print(f''' * {table} Report Read.''')
    error = ''
    cursor.execute(f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}';''')  
    colName = cursor.fetchall()
    cursor.execute(f'''SELECT * FROM {table};''')
    colRow = cursor.fetchall()
    db_conn.close()
  return colName, colRow, error

def createForm(db, user, password, table):
  error = f'''{table} Form Does Not Exist.'''
  sql = ''
  db_conn = DB(db, user, password).connect()
  cursor = db_conn.cursor(buffered=True)
  cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N'{table}'; ''')
  check_table = cursor.fetchone()
  if check_table is not None:
    print(f''' * {table} Form Generated.''')
    error = f'''Please fill in all the boxes'''
    cursor.execute(f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}' AND COLUMN_NAME NOT LIKE 'timestamp' AND COLUMN_KEY NOT LIKE 'PRI' AND COLUMN_NAME NOT LIKE 'updated';''')
    sql = cursor.fetchall()
    db_conn.close()
    if request.method == 'POST':
      try:
        colName = tuple(l[0] for l in sql)
        key = ", ".join(colName)
        value = tuple(request.values.get(l[0]) for l in sql)
        db_conn = DB(db, user, password).connect()
        cursor = db_conn.cursor(buffered=True)
        cursor.execute(f'''INSERT INTO {table} ({key}) VALUES {value};''')
        db_conn.commit()
        db_conn.close()
      except:
        error = f'''You must fill in all the boxes.'''
  return error, sql
