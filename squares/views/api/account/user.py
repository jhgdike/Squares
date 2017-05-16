from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from squares.models.account.account import Account

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/me')
@login_required
def me():
    user = Account.get(current_user.id)
    return jsonify(username=user.username)


@bp.route('/login', methods=('POST',))
def login():
    username = request.form['username']
    password = request.form['password']
    Account.check(username, password)
    Account.login(username)
    return jsonify(success=True)


@bp.route('/logout')
@login_required
def logout():
    current_user.logout()
    return jsonify(success=True)
