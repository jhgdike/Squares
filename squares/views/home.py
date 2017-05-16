from flask import Blueprint, request, render_template


bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    code = request.args.get('code')
    return render_template('index.html', **locals())
