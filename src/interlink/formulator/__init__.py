'''
The formulator is used as the SQL engine to gather the data from the database to populate the template.

The formulator module makes use of the `Generator()` object, to connect to the database, find the proper table, query the results, and return a value that can be passed into an html template. It is the main module behind the Interlink library. It acts as the SQL engine, to generate a return value, that can be manipulated to the developers needs. It's main dependancy is the `toolkit.DB()` object for connection to a database. Make sure you have the proper environment variables set to ensure proper connection. If the project does not fit into the `templetonBP` this module will assist in automating redundant SQL statements, form, and report development, and navigation menus which need to sort administration, from users, from bad actors. It can be used along side other modules in the library as well as imported directly into your own project.

Classes:  
  Generator: Object method used to query database  

'''

from .generator import Generator
