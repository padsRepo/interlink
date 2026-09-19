import os
from flask import Blueprint, render_template, request
from interlink.formulator import Generator
from interlink.safeHaven import backdoor, login, honeypot
from interlink.toolkit import DB
from interlink.templeton.decorator import templetonWrapper

templates = os.path.dirname(__file__) + '/templates/'
static = os.path.dirname(__file__) + '/static/'
templetonBP = Blueprint('templeton', __name__, url_prefix='/', template_folder=templates, static_folder='static', static_url_path='/assets/')

# Interlink data sheet
@templetonBP.route('/interlink/')
@templetonWrapper('data.html')
def data():
  '''interlink.templeton.route.data(): http://site:port/interlink/'''
  from interlink import dataCard
  return dataCard['routeData']

# Interlink license
@templetonBP.route('/interlink/license/')
@templetonWrapper('license.html')
def license():
  '''interlink.templeton.route.license(): http://site:port/interlink/license/'''
  pass

# Interlink wiki
@templetonBP.route('/interlink/wiki/<page>', defaults={'page': 'index.html'})
@templetonBP.route('/interlink/wiki/<page>')
def documentation(page):
  '''interlink.templeton.route.documentation(page): http://site:port/interlink/wiki/{page}'''
  return render_template('guide/' + page)

# Error handling
@templetonBP.errorhandler(404)
@templetonWrapper('404.html')
def url_not_found(e):
  '''interlink.templeton.route.url_not_found(e): http://site:port/404/'''
  return dict(title="** This Page Does Not Exist **", description="I can\'t find that URL...", error=f'''{e}'''), 404

@templetonBP.errorhandler(500)
@templetonWrapper('500.html')
def internal_error(e):
  '''interlink.templeton.route.internal_error(e): http://site:port/500/'''
  return dict(title="** There is an error with my code **", description="There\'s something wrong with me...Some programmer made a K18 error....", error=f'''{e}'''), 500

# Reports
@templetonBP.route('/reports/<db>/<table>')
@backdoor
@login
@honeypot
@templetonWrapper('reports.html')
def generateReport(db, table):
  '''interlink.templeton.route.generateReport(db, table): http://site:port/reports/{db}/{table}'''
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  colName, colRow, error, title = gen.generateReport(table)
  return dict(colName=colName, colRow=colRow, error=error, title=title)

# Forms
@templetonBP.route('/forms/<db>/<table>', methods=['GET', 'POST'])
@backdoor
@login
@honeypot
@templetonWrapper('forms.html')
def generateForm(db, table):
  '''interlink.templeton.route.generateForm(db, table): http://site:port/forms/{db}/{table}'''
  gen = Generator(db, 'DB_USER', 'DB_PASS')
  error, colName, lookupTable = gen.generateForm(table)
  return dict(lookupTable=lookupTable, colName=colName, error=error)

# Admin
@templetonBP.route('/admin/<db>')
@backdoor
@login
@honeypot
@templetonWrapper('admin.html')
def admin(db):
  '''interlink.templeton.route.admin(db): http://site:port/admin/{db}/'''
  nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
  return dict(nav=nav, db=db, title=db)

# Honeypot Login
@templetonBP.route('/loginRequired/', methods=['GET', 'POST'])
@templetonWrapper('login.html')
def loginRequired():
  '''interlink.templeton.route.loginRequired(): POST http://site:port/loginRequired/'''
  message = 'Please Log in'
  if request.method == 'POST':
    fakeName = request.form['username']
    fakePass = request.form['password']
    message = "Your Username or Password is incorrect"
    print(' * The user is attempting to log in!\n   User:', fakeName, 'Password:', fakePass)
    print(' * The user is attempting to log in!\n   User:', fakeName, 'Password:', fakePass, file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
  return dict(message=message)

# Real Login
@templetonBP.route('/login/', methods=['GET', 'POST'])
@templetonWrapper('login.html')
def secure_login():
  '''interlink.templeton.route.secure_login(): POST http://site:port/login/'''
  message = 'This is a Secure Login'
  if request.method == 'POST':
    session['username'] = request.form['username']
    session['passwd'] = request.form['password']
    try:
      db_conn = DB(db, user, password).connect()
      cursor = db_conn.cursor()
      cursor.execute(f'''SELECT passwd FROM profile WHERE username = "{ session['username'] }";''')
      p = cursor.fetchone()
      if pwHash.check_password_hash(p[0], session['passwd']):
        sql = f'''SELECT username, passwd FROM profile WHERE username = "{ session['username'] }" AND passwd = "{ p[0] }";'''
        cursor.execute(sql)
        sql = cursor.fetchone()
        db_conn.close()
        if sql is not None:
          message = 'You are logged in.'
          return redirect(url_for('/.index'))
        else:
          print('User does not exist.')
          return wrapper('login.html')
    except:
      print(' * The user is attempting to log in!\n   User:', session['username'])
      print(' * The user is attempting to log in!\n   User:', session['username'], file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
      message = "Your Username or Password is incorrect"
  return dict(message=message)

# Register User
@templetonBP.route('/register/', methods=['GET', 'POST'])
@templetonWrapper('register.html')
def secure_registration(db, user, pw):
  '''interlink.templeton.route.secure_registration(db, user, pw): POST http://site:port/register/'''
  error = 'This is a Secure Registration'
  print('this')
  if request.method == 'POST':
    print('that')
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    db_conn = DB(db, user, pw).connect()
    cursor = db_conn.cursor()
    cursor.execute(f'''SELECT ROW_COUNT() FROM profile;''')
    row_count = cursor.fetchall()
    if row_count is None:
      error = '** Registration is closed. Contact the Administator. **'
    else:
      #try:
        pass_hash = pwHash.generate_password_hash(password).decode('UTF-8')
        print(pass_hash)
        #salt = os.urandom(32)
        sql = f'''INSERT INTO profile(name, username, passwd, email) VALUES("{ name }", "{ username }", "{ pass_hash }", "{ email }");'''
        cursor.execute(sql)
        db_conn.commit()
        db_conn.close()
        print("Someone has made a profile!")
        print("Someone has made a profile!", file=open(os.environ.get('LOG_DIR') + '/pads.log', 'a'))
        return redirect(url_for('/.login'))
      #except:
        print('No.')
  else:
    error = 'Something went wrong.'
  return dict(error=error)
