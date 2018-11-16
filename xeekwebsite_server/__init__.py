import os
from flask import Flask
from . import index
from .view import home
from .view import article
from .view import auth

from xeekwebsite_server.LogFactory import LogInfo

import time

def creat_app(config = None):
    app = Flask(__name__,instance_relative_config=True)
    #logging.basicConfig(filename="./log/log.txt",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'xeekweb.sqlite.db'),
    )
    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.add_url_rule('/','home.index')
    app.register_blueprint(home.bp)
    app.register_blueprint(article.bp)
    app.register_blueprint(auth.bp)
    #app.add_url_rule('/index', endpoint='index2',view_func = index.index)
    app.register_blueprint(index.bp)
    
    LogInfo().init_log(app)

    return app


