def templetonWrapper(template=None):
  '''
Used to wrap all the web pages in default params.

Args:
    template(str): Passes the var to render_template

Examples:
    ```python
    @app.route('/')
    def index():
        return render_template('index.html', value=42)
    
    # This will look for a template called license.html with no parameters
    @app.route('/license/')
    @templetonWrapper()
    def license():
      pass
    
    @app.route('/')
    @templetonWrapper('index.html')
    def index():
        return dict(value=42)
    
    # In this case, the wrapper will search for a file called index.html in your templates directory.  
    @app.route('/')
    @templetonWrapper()
    def index():
        return dict(value=42)
    ```
  '''
  from functools import wraps
  from flask import request, render_template, session
  from interlink import __version__, __updated__, __author__
  from interlink.formulator import Generator
  from interlink.toolkit import site_map
  
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      page = template
      ip = request.remote_addr
      database = None
      if 'yourballslooklikemine' in session:
        database = Generator('', 'DB_USER', 'DB_PASS').generateURL()
      if page is None:
        page = f"{request.url_rule}.html"
      ctx = f(*args, **kwargs)
      print(__name__, __package__, __file__)
      if ctx is None:
        ctx = {}
      elif not isinstance(ctx, dict):
        return ctx
      return render_template(page, version=__version__, updated=__updated__, author=__author__, siteMap=site_map(), ip=ip, database=database, **ctx)
    return decorated_function
  return decorator