from flask import Blueprint
from .api import setup_api_routes, setup_main_route

def register_blueprints(app):
    api_blueprint = Blueprint('api', __name__, static_folder='dist', template_folder='dist', url_prefix='/api')
    main_bp = Blueprint('main', __name__, static_folder='dist', template_folder='dist')
    setup_api_routes(api_blueprint)
    app.register_blueprint(api_blueprint)
    setup_main_route(main_bp)
    app.register_blueprint(main_bp)
