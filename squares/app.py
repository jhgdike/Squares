import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from werkzeug.utils import import_string

from config import config


blueprints = [
    'squares.views.home:bp',
    'squares.views.api.account.user:bp',
]

extensions = [
    'squares.ext:db',
    'squares.ext:mail',
    'squares.ext:cache',
]


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for blueprint_qualname in blueprints:
        blueprint = import_string(blueprint_qualname)
        app.register_blueprint(blueprint)

    for extension_qualname in extensions:
        extension = import_string(extension_qualname)
        extension.init_app(app)

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

    return app
