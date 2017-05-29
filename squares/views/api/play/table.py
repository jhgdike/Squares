from flask import jsonify, request, render_template

from squares.views.api import create_blueprint
from squares.controllers.table import TableController, Table
from squares.views.schema.table import table_schema

bp = create_blueprint('play', 'table', __name__)


@bp.route('/home')
def home():
    """all of the tables"""
    table_ids = Table.get_all()
    return jsonify(success=True, data={'table_ids': table_ids})


@bp.route('/create')
def create():
    """create a game table"""
    player_id = request.cookies['player_id']
    table = Table.create_table(player_id)
    data = table_schema.dump(table).data
    return render_template('table.html', **data)


@bp.route('/join/<int:table_id>')
def join(table_id):
    """join"""
    player_id = request.cookie['player_id']
    tc = TableController(table_id)
    tc.join(player_id)
    data = table_schema.dump(tc).data
    return render_template('table.html', **data)


@bp.route('/observe/<int:table_id>')
def observe(table_id):
    """observer"""
    tc = TableController(table_id)
    return jsonify(success=True, data=table_schema.dump(tc).data)


@bp.route('/step/<int:table_id>')
def step(table_id):
    tc = TableController(table_id)
    schema_id = request.args.get('schema_id')
    position = request.args.get('position')
    rotate = request.args.get('rotate', type=int)
    symmetry = request.args.get('symmetry', type=bool)

    tc.step(schema_id, position, rotate, symmetry)
    return jsonify(success=True, data=dict(squares=tc.squares))


@bp.route('/ready/<int:table_id>')
def ready(table_id):
    tc = TableController(table_id)
    tc.start()
    return jsonify(success=True, data=table_schema.dump(tc).data)
