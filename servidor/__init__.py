from flask import Flask, g
from .database import init_db, get_session
from .blueprints import register_blueprints

from .config import DevelopmentConfig, TestingConfig, ProductionConfig

from .config import set_default_config

def create_app(config_name='production'):
    app = Flask(__name__, static_folder='dist', template_folder='dist')

    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    app.config.from_object(configs[config_name])

    register_blueprints(app)
    with app.app_context():
        init_db(app)
        set_default_config()

    @app.before_request
    def create_session():
        g.session = get_session()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.teardown_request
    def shutdown_session(exception=None):
        g.session.close()

    return app

