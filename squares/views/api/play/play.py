from flask import jsonify, request
from squares.views.api import create_blueprint

bp = create_blueprint('play', 'play', __name__)


@bp.route('/put', methods=('POST',))
def put():
    """put a shape into table"""
    # table_id
    # player_id
    # token
    return jsonify(succuess=True, table_id=1)


@bp.route('/cancel', methods=('POST',))
def cancel():
    """cancel the last step"""
    username = request.form['username']
    return jsonify(succuess=True, username=username, table_id=1)


@bp.route('/details')
def player_details():
    """player's shape details"""
    return jsonify(table_id=1)
