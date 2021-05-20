from flask import Blueprint, render_template
from flask import session, g
from studycam.models import User
from studycam import db
from studycam.models import StudyLog
import pandas as pd
from sqlalchemy import and_


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


@bp.route('/total/')
def total():
    data = db.engine.execute(f"SELECT   lecture_id "
                             f"       , lecture_part "
                             f"       , AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , COUNT(*)"
                             f"FROM     study_log "
                             f"WHERE    teacher_id = {session.get('user_id')} "
                             f"GROUP BY lecture_id "
                             f"       , lecture_part")

    for row in data:
        print(row)
    return render_template('teacher/total.html')
