from squares.ext import redis
from flask import (
    Blueprint, request, render_template, jsonify, make_response, redirect)

from squares.errors import BaseError
from squares.models.play.table import Table


bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    table_ids = Table.get_all()
    return render_template('index.html', table_ids=table_ids)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    name = request.form['name']
    redis.setnx(name, 1)
    # if not redis.setnx(name, 1):
    #     return render_template('login.html', error='Name has been used!')
    response = make_response(redirect('/'))
    response.set_cookie('player_id', name)
    return response


@bp.app_errorhandler(BaseError)
def app_errorhandler(e):
    return jsonify(success=False, error=str(e))


@bp.app_errorhandler(400)
@bp.app_errorhandler(401)
@bp.app_errorhandler(403)
@bp.app_errorhandler(404)
@bp.app_errorhandler(405)
@bp.app_errorhandler(410)
@bp.app_errorhandler(429)
@bp.app_errorhandler(503)
def error_handler(e):
    if request.path.startswith('/api/'):
        return jsonify(success=False, error=str(e)), e.code
    return render_template('error.html', error=str(e)), e.code
