'''
Templeton is like the butler used to fetch the templates, fill in the proper parameters, and serve it to you on a silver platter. Templeton builds the skeleton website for you. All you have to do is type in the proper URL, or generate the navigation bar.

The easiest way to use templeton is to register its Blueprint's in your app. 

Classes:    
    Tempulation: Custom Views  

Functions:  
    tempulator: templates   
    url_not_found: 404 Error  
    internal_error: 500 Error  
    templetonBP: Templeton Templates  
    interlinkAPI: API requests  
    templetonWrapper: Wrap pages in a template  
  
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


'''
from werkzeug.utils import import_string, cached_property

class Tempulation:
  '''
Generate a new url_rule from any view within your project. This is used if you would like to map out url rules for each of your own endpoints.  

Examples:

    # Use the Tempulation's to create a new URL:
    app.add_url_rule('/dash', view_func=Tempulation('interlink.templeton.views.dashboard'))

    # make a new tempulator
    def myNewTempulator(import_name, url_rules=[], **options):
        view = Tempulation(f"@{app_name@}.@{import_name@}")
        for url_rule in url_rules:
          app.add_url_rule(url_rule, view_func=view, **options)

  '''

  def __init__(self, import_name, **variables):
    '''
Initialize the Tempulation object. This will hold the variable for the new url_rule.  
  
Args:  
    object (str): Endpoint for new view
    '''
    self.__module__, self.__name__ = import_name.rsplit(".", 1)
    self.import_name = import_name
    self.variables = variables

  @cached_property
  def view(self):
    return import_string(self.import_name)

  def __call__(self, *args, **kwargs):
    kwargs.update(self.variables)
    return self.view(*args, **kwargs)


def tempulator(app, import_name, url_rules=None, **variables):
  '''
The tempulator is used to add extra templates to the app, if needed, without added overhead to the base project. For example, if you make a blog, you should be able to build a blog without also loading the catalog from an ecommerce site into memory, and vice versa. By using the tempulator, you can load a blog without a journal, or a ecommerce site without a repository, or a snosberry without an everlasting gobbstopper. You can also use the tempulator to load one endpoint before the other. If you like templetons catalog view, and you're an ecommerce site you may want to load that as your index page. This would achieve those results.

    --> views.py  
    # add a single route to the catalog view
    tempulator(app, 'interlink.templeton.views.blog', ['/api/'], db='blog', table='blog')

    # add two routes to a single function endpoint
    url_rules = ['/catalog/','/catalog/<item>']
    tempulator('views.catalog', url_rules, app = app)
  
  '''
  if url_rules is None:
    url_rules = []

  view = Tempulation(import_name, **variables)

  for url_rule in url_rules:
    app.add_url_rule(url_rule, view_func=view)
  return view
