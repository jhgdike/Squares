from flask import Blueprint, jsonify, request, redirect, url_for
from squares.libs.env_config import get_config


def create_blueprint(module, name, package_name):
    """Creates blueprint to sort the API views.

    :param name: The endpoint name.
    :param module: The module name.
    :param package_name: Always be ``__name__``.
    """

    url_prefix = '/api/{}/{}'.format(module, name)
    blueprint_name = 'api-{}.{}'.format(module, name)
    blueprint = Blueprint(
        blueprint_name, package_name, url_prefix=url_prefix)

    config = get_config('squares')

    if not config['DEBUG']:
        @blueprint.errorhandler(KeyError)
        def handle_key_error(error):
            return jsonify(success=False, error=str(error)), 400

        @blueprint.errorhandler(ValueError)
        def handle_value_error(error):
            return jsonify(success=False, error=str(error)), 400

    @blueprint.before_request
    def check_player_id():
        if not request.cookies.get('player_id'):
            return redirect(url_for('home.login'))

    return blueprint
