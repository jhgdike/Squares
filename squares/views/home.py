from flask import Blueprint, request, render_template, jsonify


bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    return render_template('index.html')


@bp.app_errorhandler(Exception)
def app_errorhandler(e):
    if request.is_xhr:
        return jsonify(success=False, error=e)
