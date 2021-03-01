import os
from flask import Flask
from newblog.settings import configs


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG' or 'dev')
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    register_bp(app)

    return app


def register_bp(app):
    from newblog.main import main
    from newblog.auth import auth
    from newblog.api import api
    from newblog.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')
