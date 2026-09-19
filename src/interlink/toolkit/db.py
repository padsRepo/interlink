
from flask import url_for
import mysql.connector
import os

class DB:
  '''
A class to interact with a MariaDB/MySQL database using environment variables for credentials.

This class provides a streamlined way to connect, execute queries, and manage database operations.
The credentials (database name, user, password) are retrieved from environment variables.
Ensure to close the connection after use to avoid resource leaks.

Args:
    db (str): Database Name
    user (str): User Name, Must be an ENV VAR
    password (str): Password, Must be an ENV VAR

Returns: 
    mydb (str): Connection to Database

Methods:  
    __init__(self, db, user, password):  
    __str__(self):  
    __repr__(self):  
    connect(self):  
    close(self):  
    cursor(self):  
    commit(self):  
    execute(self, sql):  
    fetchall(self, sql):  
    fetchone(self, sql):  
    getTableData(self, table):  
    getColumnData(self, table, where=""):  
    getKeyData(self, table):  
    getDescription(self, table):  
    getEnumData(self, table):  
    getLookupData(self, table):  

Example:
```python
    os.eviron['library'] = 'library'
    os.eviron['user'] = 'franklin'
    os.eviron['password'] = 'aklsdjhashdfsajkdfh'
    @viewsBP.route('/report/<db>/<page>')
    def myFuntion(db, user, password):
      db_conn = DB(db, user, password).connect
      cursor = db_conn.cursor(buffered=True)
      cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{db}'; ")
      sql = cursor.fetchone()
      db_conn.close
      return sql
```
  '''
  def __init__(self, db, user, password):
    '''
    Initialize the database connection using environment variables.

    Args:
        db (str): Name of the variable for the database name.
        user (str): Name of the environment variable for the database user.
        password (str): Name of the environment variable for the database password.

    Raises:
        Exception: If the connection to the database fails.

    Note:
        This method retrieves values from the environment variables and establishes a connection.
        Ensure that the environment variables are set correctly before instantiation.
    '''
    try:
      self.mydb = mysql.connector.connect(
        host = 'localhost',
        database = db,
        user = os.environ.get(user),
        password = os.environ.get(password)
      )
    except Exception as e:
      print(f"Database connection failed: {e}")
      raise
  def __str__(self):
    """
    Return the name of the database as a string.

    Returns:
        str: The name of the connected database.
    """
    return f'{self.mydb.database}'
  def __repr__(self):
    """
    Return a string representation of the DB instance.

    Returns:
        str: A formatted string with the database name, user, and password.
    """
    return f' * class DB: {__file__}\n * DB({self.user} {self.password} {self.db})'

  @property
  def connect(self):
    """
    Get the database connection object.

    Returns:
        mysql.connector.connection: The active database connection.

    Raises:
        Exception: If the connection is not established.
    """
    try:
      return self.mydb
    except:
      print("Cannot connect to DB")

  @property
  def close(self):
    """
    Close the database connection if it is open.

    This method ensures the connection is properly closed to avoid resource leaks.
    """
    if self.mydb is not None:
      self.mydb.close()

  @property
  def cursor(self):
    """
    Create and return a cursor object for executing SQL queries.

    Returns:
        mysql.connector.cursor.DictCursor: A cursor object with dictionary-style results and buffered execution.

    Note:
        This cursor supports `fetchall()` and `fetchone()` for retrieving query results.
    """
    return self.mydb.cursor(dictionary=True, buffered=True)

  def commit(self):
    """
    Commit the current transaction to the database.

    This method ensures that any changes made via the cursor are permanently saved.
    """
    return self.connect.commit()

  def execute(self, sql):
    """
    Execute a SQL query and return the cursor.

    Args:
        sql (str): The SQL query to execute.

    Returns:
        mysql.connector.cursor.DictCursor: The cursor object after executing the query.

    Raises:
        Exception: If the query execution fails.
    """
    c = self.cursor
    c.execute(sql)
    return c

  def fetchall(self, sql):
    """
    Execute a query and return all results.

    Args:
        sql (str): The SQL query to execute.

    Returns:
        list: A list of rows returned by the query (each row is a dictionary).

    Raises:
        Exception: If the query execution or result retrieval fails.
    """
    return self.execute(sql).fetchall()

  def fetchone(self, sql):
    """
    Execute a query and return the first row.

    Args:
        sql (str): The SQL query to execute.

    Returns:
        dict: A single row from the query result, or None if no rows are found.

    Raises:
        Exception: If the query execution or result retrieval fails.
    """
    return self.execute(sql).fetchone()

  def getTableData(self, table):
    """
    Retrieve metadata about a specific table.

    Args:
        table (str): The name of the table to query.

    Returns:
        list: A list of rows containing table metadata (e.g., schema, name, type, rows).

    Note:
        This queries the `INFORMATION_SCHEMA.TABLES` to fetch metadata.
    """
    sql = f'''SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE, ROW_FORMAT, TABLE_ROWS,  AUTO_INCREMENT, CREATE_TIME, UPDATE_TIME, TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{self.connect.database}' AND TABLE_NAME = N'{table}';'''
    return self.fetchall(sql)

  def getColumnData(self, table, where=""):
    """
    Retrieve metadata about columns in a specific table.

    Args:
        table (str): The name of the table to query.
        where (str): Optional WHERE clause for filtering results.

    Returns:
        list: A list of rows containing column metadata (e.g., name, type, key).

    Note:
        This queries the `INFORMATION_SCHEMA.COLUMNS` to fetch metadata.
        Excludes timestamps and primary keys by default.
    """
    sql = f'''SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, TRIM(LEADING 'enum(' FROM TRIM(TRAILING ')' FROM COLUMN_TYPE)) AS COLUMN_TYPE, COLUMN_KEY, COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = N'{self.connect.database}' AND TABLE_NAME = N'{table}' {where};'''
    try:
      return self.fetchall(sql)
    except Exception as e:
      return e

  def getKeyData(self, table):
    """
    Retrieve primary key and foreign key information for a specific table.

    Args:
        table (str): The name of the table to query.

    Returns:
        list: A list of rows containing key metadata (e.g., constraint name, referenced tables).

    Note:
        This queries the `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` to fetch key data.
    """
    sql = f'''SELECT CONSTRAINT_NAME, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION,  REFERENCED_TABLE_SCHEMA, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = N'{self.connect.database}' AND TABLE_NAME = N'{table}';'''
    return self.fetchall(sql)

  def getDescription(self, table):
    """
    Get the structure (description) of a table using the DESCRIBE command.

    Parameters:
        table (str): The name of the table to describe.

    Returns:
        list: A list of rows describing the table structure (e.g., column names, types).

    Note:
        This is equivalent to the `DESCRIBE` SQL command.
    """
    sql = f'''DESCRIBE {self.connect.database}.{table}'''
    return self.fetchall(sql)

  def getEnumData(self, table):
    """
    Retrieve ENUM column data for a specific table.

    Args:
        table (str): The name of the table to query.

    Returns:
        list: A list of rows containing ENUM column data.

    Note:
        This method is a placeholder. Consider using lookup tables instead for clarity.
    """
    import re
    sql = f'''select COLUMN_NAME as Field, TRIM(LEADING 'enum(' FROM TRIM(TRAILING ')' FROM column_type)) as Type from information_schema.columns col where table_schema = 'tFood' and table_name = 'rawMaterials' and data_type = 'enum';'''
    r = self.fetchall(sql)
    return r

  def getLookupData(self, table):
    """
    Retrieve lookup table information for a specific table based on foreign keys.

    Args:
        table (str): The name of the table to query.

    Returns:
        list: A list of rows containing lookup table details (e.g., referenced table name).

    Note:
        This method identifies foreign key relationships and retrieves lookup tables.
    """
    sql = f'''SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = N'{self.connect.database}' AND TABLE_NAME = N'{table}' AND CONSTRAINT_NAME LIKE N'FK_%';'''
    try:
      conn = self.mydb.cursor(buffered=True)
      conn.execute(sql)
      col, tbl, ref = conn.fetchall()[0]
      conn.execute(f"select * from {tbl}")
    except:
      print(" * No lookup table found.")
    return conn.fetchall()