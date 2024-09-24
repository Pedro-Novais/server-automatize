from flask import Blueprint, request, g
from config.database import init_connect
from .user import user_route
from .login import login_route
from .register import register_route
from .team import team_route
from .project import project_route

def init_routes(app):
    app.register_blueprint(user_route, url_prefix='/api/user')
    app.register_blueprint(login_route, url_prefix='/api/login')
    app.register_blueprint(register_route, url_prefix='/api/register')
    app.register_blueprint(team_route, url_prefix='/api/team')
    app.register_blueprint(project_route, url_prefix='/api/project')

    @app.before_request
    def before_request():
        g.db, g.client = init_connect()

    @app.teardown_request
    def teardown_request(exception):
            if hasattr(g, 'db'):
                g.db.client.close()
