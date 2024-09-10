from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

import os
from dotenv import load_dotenv
from flask import Flask 

import logging
from flask_talisman import Talisman
from prometheus_client import Counter, Histogram, generate_latest
from werkzeug.middleware.proxy_fix import ProxyFix


load_dotenv()


REQUEST_COUNT=Counter('request_count', 'Total number of HHTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY=Histogram('request_latency_seconds', 'Request latency', ['endpoint'])



def create_app():
    app=Flask(__name__)
    
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
    
    Talisman(app, content_content_policy=None)
    
    
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in $(pathname)s:%(lineno)d]'
    )
    
    console_handler=logging.StreamingHandler()
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)
    
    
    @app.before_request
    def before_request():
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()
        
    @app.after_request
    def after_request(response):
        REQUEST_LATENCY.labels(endpoint=request.path).observe(response.elapsed.total_seconds())
        return response 
    
    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype='text/plains')
    
    from .routes import main
    app.register_blueprint(main)
    
    
    app.wsgi_app=ProxyFix(app.wsgi_app)
    
    
    return app

db=SQLAlchemy()
login_manager=LoginManager()
login_manager.login_view="login"

def createe_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app 