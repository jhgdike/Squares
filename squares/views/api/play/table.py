from flask import jsonify, request

from squares.views.api import create_blueprint
from squares.controllers.table import TableController, Table
from squares.views.schema.table import table_schema

bp = create_blueprint('play', 'table', __name__)


@bp.route('/home')
def home():
    """all of the tables"""
    table_ids = Table.get_all()
    return jsonify(success=True, data={'table_ids': table_ids})


@bp.route('/create', methods=('POST',))
def create():
    """create a game table"""
    player_id = request.cookies['player_id']
    table = Table.create_table(player_id)
    print(table.table_id)
    return jsonify(success=True, data=table_schema.dump(table).data)


@bp.route('/join/<int:table_id>', methods=('POST',))
def join(table_id):
    """join"""
    player_id = request.cookie['player_id']
    tc = TableController(table_id)
    tc.join(player_id)
    return jsonify(success=True, data=None)


@bp.route('/observe/<int:table_id>')
def observe(table_id):
    """observer"""
    tc = TableController(table_id)
    return jsonify(success=True, data=dict(squares=tc.squares))


@bp.route('/step/<int:table_id>')
def step(table_id):
    tc = TableController(table_id)
    schema_id = request.form['schema_id']
    position = request.form['position']
    tc.step(schema_id, position)
    return jsonify(success=True, data=dict(squares=tc.squares))
