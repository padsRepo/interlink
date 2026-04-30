'''
The formulator is used as the SQL engine to gather the data from the database to populate the template.

The formulator module makes use of the `Generator()` object, to connect to the database, find the proper table, query the results, and return a value that can be passed into an html template. It is the main module behind the Interlink library. It acts as the SQL engine, to generate a return value, that can be manipulated to the developers needs. It's main dependancy is the `toolkit.DB()` object for connection to a database. Make sure you have the proper environment variables set to ensure proper connection. If the project does not fit into the `templetonBP` this module will assist in automating redundant SQL statements, form, and report development, and navigation menus which need to sort administration, from users, from bad actors. It can be used along side other modules in the library as well as imported directly into your own project.

Let's say you dont like templetons blog template and you want to use your own blog template. Use the `formulator.Generator` to make a query of your blog table from your SQL database. Create a variable from it, and then using Jinja's Templating Engine with Flask, we can manipulate the variable in an html template anyway we want.

In your views.py file you only need two specific views that will generate every form, and report respectively. In the `index()` function you will see the nav variable set to `generateNav()`. This generates the navigation bar for you. It can be used in the template to build the navigation menu. If you're familiar with flask's Blueprints, then this should look pretty simple. If not, check out the flask docs, it's pretty cool.

Basically, make a route for a reports url and a route for a forms url so that the computer doesn't confuse the two. For your route you need to define a parameter for your database, and table. This is just to pass into the `generateReport()` or `generateForm()` functions which is used to find the table, and create the form or report. The report needs 4 parameters(One for the column names of the table, one for the data in the table, a title, and a generic error) and the form needs 3(One to generate the forms, a title, and a generic error). The `generateNav()` doesn't need a parameter, but it searches for the database you set to your `Generator.__init__()`. Make sure to register the views:

```python
    __init__.py

      from views import viewsBP
      app.regist_blueprint(viewsBP)
```
```python
    views.py

      from flask import Blueprint, render_template
      import interlink as i

      viewsBP = Blueprint('/', __name__, url-prefix='/')

      @viewsBP.route(/)
      def index():
        gen = i.Generator('DB', 'DB_USER', 'DB_PASS')
        nav = gen.generateNav()
        return render_template('index.html', nav=nav)

      @viewsBP.route('/<db>/<table>')
      def blog(db, table):
        gen = Generator(db, 'DB_USER', 'DB_PASS')
        content = gen.generateQuery(table)
        return render_template('template.html', content=content)

      @viewsBP.route('/reports/<db>/<table>')
      def generateReport(db, table):
        gen = i.Generator(db, 'DB_USER', 'DB_PASS')
        colName, colRow, error, title = gen.generateReport(table)
        return render_template('reports.html', colName=colName, colRow=colRow, error=error, title=title)

      @viewsBP.route('/forms/<db>/<table>', methods=['GET', 'POST'])
      def generateForm(db, table):
        gen = i.Generator(db, 'DB_USER', 'DB_PASS')
        error, form, title = gen.generateForm(table)
        return render_template('forms.html', form=form, error=error, title=title)

      @viewsBP.route('/admin/<db>')
      def admin(db):
        nav = Generator(db, 'DB_USER', 'DB_PASS').generateNav()
        return render_template('admin.html', nav=nav, db=db, title=db)
```
Make a template for your Forms:  
```jinja
      forms.html

      {% extends 'base.html' %}
      {% block description %}{% endblock %}
      {% block keywords %}{% endblock %}
      {% block title %}{{ title }}{% endblock %}

      {% block content %}

      <article class="index">
        <section class="col-6 col-s-6 col-m-6">
          <fieldset class="form">
            <label>{{ error }}</label>
            <form method="POST">
              {% for f in form %}
                <label for="{{ f[0] }}">{{ f[0] }}</label>
                <input type="text" name="{{ f[0] }}">
              {% endfor %}
              <input type="submit" value="submit">
            </form>
          </fieldset>
        </section>
      </article>

      {% endblock %}
```
Make a template for your reports:  
```jinja
      reports.html

      {% extends 'base.html' %}
      {% block description %}{% endblock %}
      {% block keywords %}{% endblock %}
      {% block title %}{{ title }}{% endblock %}

      {% block content %}

        <article class="col-12 col-s-12 col-m-12">
          <h1>{{ title }} Report</h1>
          {{ error }}
          <table class="data">
            <tr>
              {% for c in colName %}
                <th>{{ c[0] }}</th>
              {% endfor %}
            </tr>
            {% for row in colRow %}
              <tr>
                {% for c in row %}
                <td>{{ c }}</td>
                {% endfor %}
              </tr>
            {% endfor %}
          </table>
        </article>

      {% endblock %}
```
Finally, make a navigation menu for it all. The formulator filters
"timestamp", "pri", "uni", "mul", "updated", and "q".
```jinja
      base.html

      <nav class="pc mobile">
        <a href="{{ url_for('/.index') }}">Index</a>
        <div class="dropdown">
          <span>Reports</span>
          <div class="dropdownContent">
            {% for p in nav %}
            <a href="{{ url_for('templeton.generateReport', db='{}'.format(db),  page='{}'.format(p[0])) }}">{{ p[0] }}</a>
            {% endfor %}
          </div>
        </div>
        <div class="dropdown">
          <span>Forms</span>
          <div class="dropdownContent">
            {% for p in nav %}
            <a href="{{ url_for('templeton.generateForm', db='{}'.format(db),  page='{}'.format(p[0])) }}">{{ p[0] }}</a>
            {% endfor %}
          </div>
        </div>
      </nav>
```
That's it! So if you have a DB with tables named books, authors,
planets, solarSystems....etc. Just type in the url for the table name.
For example:

`https://www.website.com/reports/library/authors`  
`https://www.website.com/reports/library/books`  
`https://www.website.com/forms/library/authors`  
`https://www.website.com/forms/library/books`  
OR  
`https://www.website.com/reports/science/solarSystems`  
`https://www.website.com/reports/science/planets`  
`https://www.website.com/forms/science/solarSystems`  
`https://www.website.com/forms/science/planets`  


'''

from .db import DB
from .generator import Generator
