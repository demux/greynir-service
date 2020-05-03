import urllib3
import logging

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from .config import Config
from .db import init_db


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)


def create_app(pre_config=None, post_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='views/templates',
    )

    app.config.from_object(Config)
    app.config.from_envvar('FLASK_CONFIG', silent=True)

    sentry_sdk.init(
        dsn=app.config.get('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        environment=app.config.get('ENVIRONMENT'),
    )

    with app.app_context():
        init_db(app)
        from . import views

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
