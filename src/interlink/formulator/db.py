import mysql.connector
import os

class DB:
  '''
The DB class is designed to facilitate operations on databases using MariaDB. It enables you to establish connections to your database with credentials that possess appropriate permissions.
Ensure you close the connection after completing your operations to avoid potential resource leaks.

Args:
    db (str): Database Name, Must be an ENV VAR
    user (str): User Name, Must be an ENV VAR
    password (str): Password, Must be an ENV VAR

Returns: 
    mydb (str): Connection to Database

Example:
```python
    os.eviron['db'] = 'library'
    os.eviron['user'] = 'franklin'
    os.eviron['password'] = 'aklsdjhashdfsajkdfh'
    @viewsBP.route('/report/<db>/<page>')
    def myFuntion(db, user, password):
      db_conn = DB(db, user, password).connect()
      cursor = db_conn.cursor(buffered=True)
      cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db}'; ")
      sql = cursor.fetchone()
      db_conn.close()
      return sql
```
  '''
  def __init__(self, db, user, password):
    '''Initialize the database object'''
    self.db = db
    self.user = user
    self.password = password
  def __str__(self):
    return f' * You are connected to your DB.'
  def __repr__(self):
    return f' * class DB: {__file__}\n * DB({self.user} {self.password} {self.db})'
    
  def connect(self):
    '''Used to make a connection to MariaDB'''
    mydb = mysql.connector.connect(
    host = 'localhost',
    database = os.environ.get(self.db),
    user = os.environ.get(self.user),
    password = os.environ.get(self.password)
    )
    return mydb
  
  def close(self):
    '''Used to close a connection to MariaDB'''
    db = DB(self.db, self.user, self.password)
    if db is not None:
      db.close()
    
class DataHandler:
  '''
The DataHandler class is designed to manage various data operations related to databases, including fetching database and table names, retrieving enumerated list data, and obtaining metadata.

Args:
    db_name (str): The name of the database.
    user (str): The username for the database connection.
    password (str): The password for the database connection.
  '''
  def __init__(self, db, user, password):
    self.db = db
    self.user = user
    self.password = password
  
  def getDatabase(self):
    '''
    Get Database Names which the user has access to.
  
    Returns:
        sql(list): A list of tuples containing database names
    '''
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    cursor.execute(f"""SHOW DATABASES WHERE `Database` NOT in ("information_schema", "performance_schema", "mysql", "sys");""")
    sql = cursor.fetchall()
    db_conn.close()
    return sql
  
  def getTables(self):
    '''
    Get Table Names from a specific Database which the user has access to.

    Returns:
        sql(list): A list of tuples containing table names.
    '''
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    cursor.execute(f''' SHOW TABLES FROM {self.db} WHERE Tables_in_{self.db} not like "q%"; ''')
    sql = cursor.fetchall()
    db_conn.close()
    return sql
          
  def getEnumData(self, table):
    '''
    Retrieve HTML options for enumerated lists from a given table.

    Args:
        table (str): The name of the table.

    Returns:
        html(str): An HTML string representing the select element.
    '''
    import re
    try:
      db_conn = DB(self.db, self.user, self.password, self.db).connect()
      cursor = db_conn.cursor(buffered=True)
      cursor.execute(f"""show COLUMNS from {table} where type like 'enum%';""")
      sql = cursor.fetchone()
      enum_list = sql[1].replace('enum(', '').replace(')', '')
      data = re.findall(r"'(.*?)'", enum_list)
      html = f'''<label for="{ sql[0] }">{ sql[0] }:</label>\n<select name="{ sql[0] }">\n'''
      for d in data:
        html += f'''  <option value="{ d }">{ d }</option>\n'''
      html += f'''</select>\n'''
      return html
    except:
      print(' * No Enumerated List for', table)
      e = ''
      return e
      
  def getMetadata(self, table):
    '''
    Obtain metadata related to foreign keys in a specified table.

    Args:
        table (str): The name of the table.

    Returns:
        html(str): An HTML string representing the select element.
    '''
    try:
      db_conn = DB(self.db, self.user, self.password, self.db).connect()
      cursor = db_conn.cursor(buffered=True)
      cursor.execute(f'''SELECT REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE   TABLE_SCHEMA = '{self.db}' and CONSTRAINT_NAME = "FK_{table}";''')
      tbleName = cursor.fetchone()
      cursor.execute(f'''SELECT * FROM {tbleName[0]};''')
      data = cursor.fetchall()
      print(data, tbleName)
      db_conn.close()
      html = f'''<label for="snid">item</label>\n<select name="snid">\n'''
      for d in data:
        html += f'''  <option value="{ d[0] }">{ d[0] } - { d[2] }</option>\n'''
      html += f'''</select>\n'''
      return html
    except:
      print(" * No Lookup Table for", table)
      e = ""
      return e
