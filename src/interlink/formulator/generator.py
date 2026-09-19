class Generator:
  '''
The generator is the module used to generate your forms, reports, queries, and anything DB related. It wraps the core functionality of the modeule into a reusable Class Object which you can use to recall a connection or query to a specifc database and table. In practice, the developer would not have to write the boilpate code needed to connect, query, and close connection to the database. By leveraging the concept of OOP, the intent is to mitigate, and slow down DDOS attacks, by preventing the end user from creating multiple concurrent conections to any given website.  

Args:  
    db (str): Database Name, Must be an ENV VAR  
    user (str): User Name, Must be an ENV VAR  
    password (str): Password, Must be an ENV VAR  

Returns:  
    200: Success
    404: Not Found
    500: Fail

Methods:  
    __init__: init  
    __str__: str  
    __repr__: repr  
    generateForm: form  
    generateReport: report  
    generateQuery: result  
    generateNav: result  
    generateURL: result  

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
  from interlink.toolkit import DB
  def __init__(self, db, user, password):
    '''Initialize the Generator object. This would, in theory, create a new object in the session which the server could point back to.'''
    self.db = self.DB(db, user, password)
  def __str__(self):
    return f' * Your Generator object is active.\n'
  def __repr__(self):
    return f'* File: {__file__}\n * Type: {type(self)}\n'

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
        @app.route('/forms/<db>/<page>', methods=['GET', 'POST'])
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
    error = f'''{table} Form Does Not Exist.'''
    colName = ''
    lookupTable = ''
    db_conn = self.db
    colName = db_conn.getColumnData(table, where=f"AND COLUMN_TYPE NOT LIKE N'timestamp' AND COLUMN_KEY NOT LIKE 'PRI'")
    if colName != []:
      print(f''' * {table} Form Generated.''')
      error = f'''Please fill in all the boxes'''
      lookupTable = db_conn.getLookupData(table)
      if request.method == 'POST':
        try:
          name = tuple(l['COLUMN_NAME'] for l in colName)
          key = ", ".join(name)
          value = tuple(request.form.get(l) for l in name)
          db_conn = db_conn.connect
          cursor = db_conn.cursor(buffered=True)
          sql = cursor.execute(f'''INSERT INTO {self.db}.{table} ({key}) VALUES {value};''')
          db_conn.commit()
          db_conn.close()
          error = f'''SUCCESS!'''
        except:
          error = f'''You must fill in all the boxes.'''
    return error, colName, lookupTable
    
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
    db_conn = self.db
    check_table = db_conn.getColumnData(table)
    if check_table is not None:
      print(f''' * {self.db}.{table} Report Read.''')
      error = ''
      colName = tuple(t for t in check_table)
      colRow = tuple(r for r in db_conn.fetchall(f'''SELECT * FROM {self.db}.{table};'''))
      conn = db_conn.connect
      cursor = conn.cursor(buffered=True)
      cursor.execute(f'''SELECT * FROM {self.db}.{table};''')
      colRow = tuple(r for r in cursor.fetchall())
      db_conn.close
    else:
      print(error)
    return colName, colRow, error, table
    
  def generateQuery(self, table, select="*", where=''):
    '''
    Run a custom SELECT statement to see the results.  
    
    TODO:  
    - Add *args to select different columns.

    Args:
    table (str): Table name to query
    select (str): List of column names to filter. List a traditional SQL Select Statement.
    where (str): List of filters.

    Returns:
    sql (str): Index of the data for each column in a record
    '''
    db_conn = self.db
    sql = db_conn.fetchall(f'''SELECT {select} FROM {self.db}.{table} {where};''')
    db_conn.close
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
                <a href="{{ url_for('templeton.generateReport', db='{}'.format(db),  page='{}'.format(p)) }}">{{ p }}</a><br>
              {% endfor %}
        </div>
        <div class="adminNav col-5">
          <h2>Forms:</h2>
              {% for p in nav %}
                <a href="{{ url_for('templeton.generateForm', db='{}'.format(db),  page='{}'.format(p)) }}">{{ p }}</a><br>
              {% endfor %}
        </div>
    ```
    '''
    db_conn = self.db
    #sql = db_conn.fetchall(f''' SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{self.db}' AND TABLE_TYPE NOT LIKE 'view'; ''')
    sql = db_conn.fetchall(f''' SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = N'{self.db}' AND TABLE_NAME NOT LIKE 'q%'; ''')
    result = tuple(s[f'TABLE_NAME'] for s in sql)
    db_conn.close
    return result

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
    db_conn = self.db
    sql = db_conn.fetchall(f"""SHOW DATABASES WHERE `Database` NOT in ("information_schema", "performance_schema", "mysql", "sys");""")
    result = tuple(s['Database'] for s in sql)
    db_conn.close
    return result
