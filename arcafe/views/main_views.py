from flask import Blueprint, render_template
from flask import session, g
from arcafe.models import User_02


bp = Blueprint('main', __name__, url_prefix='/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User_02.query.get(user_id)


@bp.route('/')
def index():
    return render_template('main/index.html')
