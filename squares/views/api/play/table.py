import json
import logging

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


@bp.route('/create', methods=('POST',))
def create():
    """create a game table"""
    player_id = request.cookies['player_id']
    table = Table.create_table(player_id)
    tc = TableController(table.table_id, player_id)

    data = table_schema.dump(tc)
    logging.info(data)
    return render_template('table.html', **data)


@bp.route('/join/<string:table_id>', methods=('POST',))
def join(table_id):
    """join"""
    player_id = request.cookies['player_id']
    tc = TableController(table_id)
    tc.join(player_id)
    data = table_schema.dump(tc)
    logging.info(data)
    return render_template('table.html', **data)


@bp.route('/observe/<string:table_id>')
def observe(table_id):
    """observer"""
    player_id = request.cookies.get('player_id', 0)
    tc = TableController(table_id, player_id)
    data = table_schema.dump(tc)
    logging.info(data)
    return jsonify(success=True, data=data)


@bp.route('/step/<string:table_id>', methods=('POST',))
def step(table_id):
    player_id = request.cookies['player_id']
    tc = TableController(table_id, player_id)
    logging.info(request.form)

    schema_id = request.form.get('schema_id', type=int)
    p_x = request.form.get('p_x', type=int)
    p_y = request.form.get('p_y', type=int)
    rotate = request.form.get('rotate', 0, type=int)
    symmetry = request.form.get('symmetry', 0, type=int)

    tc.step(schema_id, [p_y, p_x], rotate, bool(symmetry))
    data = table_schema.dump(tc)
    logging.info(data)
    return jsonify(success=True, data=data)


@bp.route('/start/<string:table_id>', methods=('POST',))
def start(table_id):
    player_id = request.cookies['player_id']
    tc = TableController(table_id, player_id)
    tc.start()
    data = table_schema.dump(tc)
    logging.info(data)
    return jsonify(success=True, data=data)


@bp.route('/quit/<string:table_id>', methods=('POST',))
def gave_up(table_id):
    player_id = request.cookies['player_id']
    tc = TableController(table_id, player_id)
    tc.quit()
    return jsonify(success=True)
