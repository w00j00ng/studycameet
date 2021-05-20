from flask import Blueprint, render_template
from flask import session, g
from studycam.models import User
from studycam import db
import pandas as pd


bp = Blueprint('teacher', __name__, url_prefix='/teacher/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/')
def index():
    return render_template('teacher/index.html')
