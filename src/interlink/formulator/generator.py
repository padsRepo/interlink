from .db import DB, DataHandler

class Generator:
  '''
The generator is the module used to generate your forms, reports, queries, and anything DB related. It wraps the core functionality of the modeule into a reusable Class Object which you can use to recall a connection or query to a specifc database and table. In practice, the developer would not have to write the boilpate code needed to connect, query, and close connection to the database. By leveraging the concept of OOP, the intent is to mitigate, and slow down DDOS attacks, by preventing the end user from creating multiple concurrent conections to any given website.

Args:
    db (str): Database Name, Must be an ENV VAR  
    user (str): User Name, Must be an ENV VAR  
    password (str): Password, Must be an ENV VAR  

Example:
```python
    @templetonBP.route('/blog/')
    @honeypot
    @backdoor
    def blog():
      gen = Generator('blog', 'DB_USER', 'DB_PASS')
      colName, colRow, error, title = gen.generateReport('blog')
      return render_template('blog.html', colName=colName, colRow=colRow, error=error, title=title)
```  

  '''
 
  def __init__(self, db, user, password):
    '''Initialize the Generator object. This would, in theory, create a new object in the session which the server could point back to.'''
    self.db = db
    self.user = user
    self.password = password
  def __str__(self):
    return f' * Your Generator object is active.\n'
  def __repr__(self):
    return f'* class Generator: {__file__}\n * Generator({self.db}, {self.user}, {self.password})\n'

  def generateForm(self, table):
    '''
    Generate a form using *table* name to populate the `form.html` template.
    
    TODO:  
    - Find better terms for the functions and values of data and enumList
    
    Args:
    table (str): Name of table within database
      
    Returns:
    error (str): 200 404 500  
    form (str): Data used to populate template   
    data (str): Finds metadata and creates a dropdown menu
    enumList(str): Finds any enumerations in SQL and creates a dropdown menu
    title (str): Name of *db* given from *__init__*

    Example:
    ```python
        @templetonBP.route('/forms/<db>/<page>', methods=['GET', 'POST'])
        @backdoor
        @login
        @honeypot
        def generateForm(db, page):
          gen = Generator(db, 'DB_USER', 'DB_PASS')
          error, form, data, enumList, title = gen.generateForm(page)
          return wrapper('forms.html', form=form, error=error, title=title, data=data, enumList=enumList)
    ```  
    '''
    from flask import request
    error = f'''{self.db}.{table} Form Does Not Exist.'''
    sql = ''
    title = table
    database = DataHandler(self.db, self.user, self.password)
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{self.db}' AND TABLE_NAME = N'{table}'; ''')
    check_table = cursor.fetchone()
    if check_table is not None:
      print(f''' * {self.db}.{table} Form Generated.''')
      error = f'''Please fill in all the boxes'''
      cursor.execute(f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = N'{self.db}' AND TABLE_NAME = N'{table}' AND COLUMN_NAME NOT LIKE 'timestamp' AND COLUMN_NAME NOT LIKE 'updated' AND COLUMN_KEY NOT LIKE 'PRI';''')
      sql = cursor.fetchall()
      db_conn.close()
      if request.method == 'POST':
        try:
          colName = tuple(l[0] for l in sql)
          key = ", ".join(colName)
          value = tuple(request.values.get(l[0]) for l in sql)
          db_conn = DB(self.user, self.password).connect()
          cursor = db_conn.cursor(buffered=True)
          cursor.execute(f'''INSERT INTO {self.db}.{table} ({key}) VALUES {value};''')
          db_conn.commit()
          db_conn.close()
          error = f'''Success!'''
        except:
          error = f'''You must fill in all the boxes.'''
    data = database.getMetadata(table)
    enumList = database.getEnumData(table)
    return error, sql, data, enumList, title
    
  def generateReport(self, table):
    '''
    Generate a report using *table* name to populate the `report.html` template.
    
    Args:
    table (str): Name of table within database
      
    Returns: 
    colName (str): Name of each column in the *table*  
    colRow (str): Data within each row of the *table*  
    error (str): 200 404 500  
    title (str): Name of *table* given from *__init__*

    Example:
    ```python
        @templetonBP.route('/reports/<db>/<page>')
        @backdoor
        @login
        @honeypot
        def generateReport(db, page):
          gen = Generator(db, 'DB_USER', 'DB_PASS')
          colName, colRow, error, title = gen.generateReport(page)
          return wrapper('reports.html', colName=colName, colRow=colRow, error=error, title=title)
    ```
    '''
    error = f'''{self.db}.{table} Report Does Not Exist'''
    colName = ''
    colRow = ''
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{self.db}' AND TABLE_NAME = N'{table}'; ''')
    check_table = cursor.fetchone()
    if check_table is not None:
      print(f''' * {self.db}.{table} Report Read.''')
      error = ''
      cursor.execute(f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = N'{self.db}' AND TABLE_NAME = N'{table}';''')
      colName = cursor.fetchall()
      cursor.execute(f'''SELECT * FROM {self.db}.{table};''')
      colRow = cursor.fetchall()
      db_conn.close()
    else:
      print(error)
    return colName, colRow, error, table
    
  def generateQuery(self, table, select="*", **kwargs):
    '''
    Run a custom SELECT statement to see the results.  
    
    TODO:  
    - Add *args to select different columns.

    Args:
    table (str): Table name to query
    select (str): List of column names to filter. List a traditional SQL Select Statement.

    Returns:
    sql (str): Index of the data for each column in a record
    '''
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    print('logic.py Ln 12', select, [k for k in kwargs])
    cursor.execute(f'''SELECT {select} FROM {self.db}.{table};''')
    sql = cursor.fetchall()
    db_conn.close()
    if sql is not None:
      print(" *", table, "Report Read.")
    else:
      sql = " * No", table, "Report"
      print(" * No", table, "Report")
    return sql
    
  def generateNav(self):
    '''
    Generate a URL for each *table* in a *db*, which the *user* has access.
    This is useful within an Admin Page, to generate a url for each form or report of the *table*.
    
    Example:  
    -> views.py
    ```python
        @templetonBP.route('/admin/<db>')
        @backdoor
        @login
        @honeypot
        def admin(db):
          nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
          return wrapper('admin.html', nav=nav, db=db, title=db)
    ```  
    -> base.html
    ```jinja
        <div class="adminNav col-5">
          <h2>Reports:</h2>
              {% for p in nav %}
                <a href="{{ url_for('templeton.generateReport', db='{}'.format(db),  page='{}'.format(p[0])) }}">{{ p[0] }}</a><br>
              {% endfor %}
        </div>
        <div class="adminNav col-5">
          <h2>Forms:</h2>
              {% for p in nav %}
                <a href="{{ url_for('templeton.generateForm', db='{}'.format(db),  page='{}'.format(p[0])) }}">{{ p[0] }}</a><br>
              {% endfor %}
        </div>
    ```
    '''
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    #cursor.execute(f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE   TABLE_SCHEMA='{db}' AND TABLE_NAME NOT LIKE 'q%'; ''')
    cursor.execute(f''' SHOW TABLES FROM {self.db} WHERE Tables_in_{self.db} not like "q%"; ''')
    sql = cursor.fetchall()
    db_conn.close()
    return sql

  def generateURL(self):
    '''
    Generate a URL for each *db*, which the *user* has access.
    This is useful to generate a navigation bar in a `base.html` file, to access each database. Which would lead you to an admin page to generate a url for each table within the database.
    
    Example:  
    -> views.py
    ```python
         @templetonBP.route('/dashboard/')
         def dashboard():
           database = Generator('', 'DB_USER', 'DB_PASS').generateURL()
           return render_template('data.html', database=database)
    ```  
    -> base.html
    ```jinja
        {% for d in database %}
          <li><a href="{{ url_for('templeton.admin', db='{}'.format(d[0])) }}" title="{{ d[0] }} Panel"><img src="{{ url_for('templeton.static', filename='/img/icons/ai-settings2-t.png') }}"><span>{{ d[0] }}</span></a></li>
        {% endfor %}
    ```
    '''
    db_conn = DB(self.db, self.user, self.password).connect()
    cursor = db_conn.cursor(buffered=True)
    cursor.execute(f"""SHOW DATABASES WHERE `Database` NOT in ("information_schema", "performance_schema", "mysql", "sys");""")
    sql = cursor.fetchall()
    db_conn.close()
    return sql
