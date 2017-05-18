import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_admin import Admin
from werkzeug.utils import import_string

from squares.libs.env_config import get_config


blueprints = [
    'squares.views.home:bp',
    'squares.views.api.account.user:bp',
]

extensions = [
    # 'squares.ext:db',
    'squares.ext:mail',
    'squares.ext:cache',
    'squares.ext:redis',
]

admin_views = [
]


def create_app(config=None):
    app = Flask('squares')
    app.config.from_pyfile('app.cfg')
    app.config.from_object(get_config('squares'))
    app.config.from_object(config)

    for blueprint_qualname in blueprints:
        blueprint = import_string(blueprint_qualname)
        app.register_blueprint(blueprint)

    for extension_qualname in extensions:
        extension = import_string(extension_qualname)
        extension.init_app(app)

    log_config(app)

    admin = Admin(app, name='神', template_mode='bootstrap3')
    for modelview_qualname in admin_views:
        modelview = import_string(modelview_qualname)
        admin.add_view(modelview)

    return app


def log_config(app):
    # log config
    log_path = app.config.get('LOG_DIR')
    if log_path:
        ch = RotatingFileHandler(
            '{}/{}_app.log'.format(log_path, app.name), 'w',
            10 * 1024 * 1024, 20)
    else:
        ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log = logging.getLogger()
    log.addHandler(ch)
