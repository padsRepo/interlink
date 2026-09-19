import os
from flask import Flask, Blueprint, render_template, url_for, request
from views import viewsBP
from interlink import appFactory

'''
def create_app():
  os.environ['BASE_DIR'] = os.path.dirname(__file__)
  os.environ['LOG_DIR'] = os.environ.get('BASE_DIR') + '/log'
  os.environ['whitelist'] = '["127.0.0.1", "192.168.1.249"]'
  os.environ['blacklist'] = '["71.71.71.71"]'
  
  app = Flask(__name__)
  app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY'))
  app.config['UPLOAD_FOLDER'] = 'repo/'
  
  import interlink as i
  
  #tempulator('views', ['/.cat'])
  app.register_blueprint(viewsBP)
  app.register_blueprint(i.templetonBP)
  app.register_error_handler(404, i.url_not_found)
  app.register_error_handler(500, i.internal_error)
  
  # print(app.url_map)
  # print(i.templetonBP.root_path)
  # print(i.__version__)
  return app
'''

app = appFactory()

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port='8081')
