from flask import jsonify, request
from squares.views.api import create_blueprint

from squares.controllers.table import TableController

bp = create_blueprint('play', 'table', __name__)
tc = TableController()


@bp.route('/home')
def home():
    """all of the tables"""
    return jsonify(success=True, tables=tc.tables())


@bp.route('/create', methods=('POST',))
def create():
    """create a game table"""
    username = request.form['username']
    return jsonify(success=True, username=username, table_id=tc.create_table())


@bp.route('/join/<int:table_id>', methods=('POST',))
def join(table_id):
    """join"""
    player_id, role_id = tc.join(table_id)
    return jsonify(
        success=True, table_id=table_id, player_id=player_id, role_id=role_id)


@bp.route('/observe/<int:table_id>')
def observe(table_id):
    """observer"""
    return jsonify(success=True, data=tc.observer(table_id))
