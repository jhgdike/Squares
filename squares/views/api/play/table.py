import json

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
    tc = TableController(table.table_id)

    data = table_schema.dump(tc).data
    # return jsonify(data)
    return render_template('table.html', **data)


@bp.route('/join/<string:table_id>')
def join(table_id):
    """join"""
    player_id = request.cookies['player_id']
    tc = TableController(table_id)
    tc.join(player_id)
    data = table_schema.dump(tc).data
    # return jsonify(data)
    return render_template('table.html', **data)


@bp.route('/observe/<string:table_id>')
def observe(table_id):
    """observer"""
    tc = TableController(table_id)
    return jsonify(success=True, data=table_schema.dump(tc).data)


@bp.route('/step/<string:table_id>')
def step(table_id):
    player_id = request.cookies['player_id']
    tc = TableController(table_id, player_id)

    schema_id = request.args.get('schema_id')
    position = json.loads(request.args.get('position', "[0, 0]"))
    rotate = request.args.get('rotate', 0, type=int)
    symmetry = request.args.get('symmetry', False, type=bool)

    tc.step(schema_id, position, rotate, symmetry)
    return jsonify(success=True, data=dict(squares=tc.squares))


@bp.route('/start/<string:table_id>')
def start(table_id):
    player_id = request.cookies['player_id']
    tc = TableController(table_id, player_id)
    tc.start()
    return jsonify(success=True, data=table_schema.dump(tc).data)


@bp.route('/quit/<string:table_id>')
def gave_up(table_id):
    player_id = request.cookies['player_id']
    tc = TableController(table_id, player_id)
    tc.quit()
    return jsonify(success=True)
