from flask import Blueprint, jsonify


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

    @blueprint.errorhandler(KeyError)
    def handle_key_error(error):
        return jsonify(success=False, error=error.messages), 400

    @blueprint.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify(success=False, error=error.messages), 400

    return blueprint
