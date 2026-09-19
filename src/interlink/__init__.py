# This file is used as a hub to import the functions of each of Interlinks API Libraries.
# Copyright Joe Corso pads.email.address@hotmail.com

"""
Flask Generator for Forms, Reports, URLs and templates.  

This is a collection of libraries written to work in Python’s flask framework. It will generate a form, report, and URL for any table in a database. It also utilizes flask's lazy loading, and API calls to generate your data in a structured format that you can customize how you want. You can build your website by generating your own instance of the API, and manipulating the data how you want. You can lazy load specific templates when you need them. Or you can register the Blueprint (e.g. app.register_blueprint(templetonBP)), which has its own set of templates for low-code solutions and rapid prototyping.  
So essentially, if you create a database for a blog with tables to organize it. You need a form, a report, a URL to get the data, and the logic to manage it. Interlink will generate the form, report, URL, and process the data. You write the database. You manage the data flow. Interlink retrieves the data from the database, the table, and fills in the details in the template. To render the page in the browser just type in the URL which corresponds to the table name, make a requests call, or make a navigation bar to generate the links for you.  
You can use the `DB` module to customize your database connections. You can use `Generator` to customize the data that loads into your template. You can use `templeton` to customize your routes and views. You can use `safeHaven` to customize access to each route. There is a set of API's to write your own methods. You can also use `tempulator` (uses flask lazy loading) to manage your own dataflow to a template.  

> [NOTE]  
> You need to ensure that you have mysql-secure-install set up, and a user with access to your databse. Setting up the database itself and CRUD is outside the scope of this documentation  

Requirements
- Install/Setup MariaDB  
- Install/Setup Virtual Env  
- Install/Setup Flask  
- Install Interlink:
```bash
    $ python -m venv path/to/venv/my_env
    $ . path/to/venv/my_env/bin/activate
    $ python -m pip install git+https://github.com/padsRepo/interlink.git
```
Setup

  **App Factory**:  
  
  ```python
    from interlink import appFactory
    from views import viewsBP
    from flask import Flask
    import os
    
    app = Flask(__name__)
    os.environ['BASE_DIR'] = os.path.dirname(__file__)
    os.environ['LOG_DIR'] = os.environ.get('BASE_DIR') + '/log'
    os.environ['whitelist'] = '["127.0.0.1", "192.168.1.249"]'
    os.environ['blacklist'] = '["71.71.71.71"]'
    app = appFactory(app, viewsBP) # Include an instance of the app. Add any of your own views
    
    if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port='8081')
  ```

  **Your Own**:  
  
  ```python
    import os
    from flask import Flask, Blueprint, render_template, url_for
    from views import viewsBP
    
    KEY = os.urandom(16)
    os.environ['SECRET_KEY'] = str(KEY) # REQUIRED
    os.environ['DB_USER'] = '<username>' # REQUIRED
    os.environ['DB_PASS'] = '<password>' # REQUIRED
    os.environ['BASE_DIR'] = os.path.dirname(__file__)
    os.environ['LOG_DIR'] = os.environ.get('BASE_DIR') + '/log'
    os.environ['whitelist'] = '["127.0.0.1", "192.168.0.37"]' # REQUIRED
    os.environ['blacklist'] = '["71.71.71.71"]' # REQUIRED
    
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY'))
    
    from interlink import templetonBP, interlinkAPI, url_not_found, internal_error
    app.register_blueprint(viewsBP) # Your views.py file
    app.register_blueprint(templetonBP) # Add to use interlinks templating engine
    app.register_blueprint(interlinkAPI) # Optional, use for API requests
    app.register_error_handler(404, url_not_found) # From the templeton lib
    app.register_error_handler(500, internal_error) # From the templeton lib
    
    if debug == False:
      app.run(debug=True, host='0.0.0.0', port='8000')
         
  ```

Modules:  
  formulator: Form and Report Generator  
  templeton: Template Generator  
  safeHaven: Security Guard  
  toolkit: Misc Tools  

Classes:  
  Generator: Object method used to query database  
  DB: Object method used to connect and close connection to database  
  Tempulation: Custom Views  

Functions:  
  tempulator: templates   
  url_not_found: 404 Error  
  internal_error: 500 Error  
  templetonBP: Templeton Templates  
  interlinkAPI: API requests
  templetonWrapper: Wrap pages in a template  
  honeypot: Redirect `blacklist` ip to a fake login page  
  backdoor: Give full access to ip on the `whitelist`  
  login: Redirect user to secure login page  
  site_map: Object method used to query database  
  get_script_path: path  
  
References:  
    interlink.templeton.api.interlinkData(): /interlink/v1  
    interlink.templeton.api.getTables(db): /interlink/v1/getTables/{db}  
    interlink.templeton.api.getTableData(db): /interlink/v1/getTableData/{db}/{table}  
    interlink.templeton.route.data(): http://site:port/interlink/  
    interlink.templeton.route.license(): http://site:port/interlink/license/  
    interlink.templeton.route.documentation(page): http://site:port/interlink/wiki/{page}  
    interlink.templeton.route.url_not_found(e): http://site:port/404/  
    interlink.templeton.route.internal_error(e): http://site:port/500/  
    interlink.templeton.route.generateReport(db, table): http://site:port/reports/{db}/{table}  
    interlink.templeton.route.generateForm(db, table): http://site:port/forms/{db}/{table}  
    interlink.templeton.route.admin(db): http://site:port/admin/{db}/  
    interlink.templeton.route.loginRequired(): POST http://site:port/loginRequired/  
    interlink.templeton.route.secure_login(): POST http://site:port/login/  
    interlink.templeton.route.secure_registration(db, user, pw): POST http://site:port/register/  
    interlink.templeton.views.data  
    interlink.templeton.views.documentation(page)  
    interlink.templeton.views.blog(db, table)  
    interlink.templeton.views.store(db, table)  
    interlink.templeton.views.generateReport(db, table)  
    interlink.templeton.views.generateForm(db, table)  
    interlink.templeton.views.admin(db)  

"""

# metadata
__version__ = '0.1.1'
__author__ = 'Joe Corso'
__date__ = '01-21-2024'
__updated__ = '02-28-2026'
__copyright__ = 'Copyright 2024 Joe Corso'
__license__ = 'MIT License'
__email__ = 'pads.email.address@gmail.com'
__status__ = 'Production'
__description__ = "Flask Generator for Forms, Reports, URLs and Templates."
#__all__ = ['formulator', 'templeton', 'safeHaven', 'toolkit']

from interlink.formulator import Generator
from interlink.templeton import Tempulation, tempulator
from interlink.templeton.api import interlinkAPI
from interlink.templeton.route import templetonBP, url_not_found, internal_error
from interlink.templeton.decorator import templetonWrapper
from interlink.safeHaven import honeypot, backdoor, login
from interlink.toolkit import site_map, DB

dataCard = {
  'apiURL': '/interlink/v1',
  'apiData': {'version': __version__, 'updated': __updated__, 'author': __author__, 'created': __date__,  'copyright': __copyright__, 'license': __license__, 'email': __email__, 'status': __status__, 'desc': __description__},
  'routeURL': '/interlink/',
  'routeData': dict(currentVersion=__version__, updatedDate=__updated__, authorName=__author__, createdDate=__date__,  copy=__copyright__, lic=__license__, emailAddress=__email__, deploymentStatus=__status__, desc=__description__),
}

def appFactory(app, bp=None):
  import os
  import interlink as i

  app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY'))
  app.config['UPLOAD_FOLDER'] = 'repo/'
  
  if bp is not None:
    app.register_blueprint(bp)
  app.register_blueprint(i.templetonBP)
  app.register_blueprint(i.interlinkAPI)
  app.register_error_handler(404, i.url_not_found)
  app.register_error_handler(500, i.internal_error)
  return app
