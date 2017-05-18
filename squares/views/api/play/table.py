from flask import jsonify, request
from squares.views.api import create_blueprint

bp = create_blueprint('play', 'table', __name__)


@bp.route('/home')
def home():
    """all of the tables"""
    return jsonify(tables=[])


@bp.route('/details/<int:table_id>')
def table(table_id):
    """one table"""
    return jsonify(table_id=table_id)


@bp.route('/create', methods=('POST',))
def create():
    """create a game table"""
    username = request.form['username']
    return jsonify(username=username, table_id=1)


@bp.route('/join/<int:table_id>', methods=('POST',))
def join(table_id):
    """join"""
    return jsonify(table_id=table_id, player_id=1, token=1)


@bp.route('/observe/<int:table_id>')
def observe(table_id):
    """join"""
    return jsonify(table_id=table_id, player_id=1, token=1)
