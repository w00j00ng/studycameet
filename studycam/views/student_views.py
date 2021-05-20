from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from studycam.models import User
from studycam import db
from studycam.models import StudyLog
import pandas as pd
from sqlalchemy import and_


bp = Blueprint('student', __name__, url_prefix='/student/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/')
def index():
    return redirect(url_for('student.total'))


@bp.route('/total/')
def total():
    data = db.engine.execute(f"SELECT   lecture_id "
                             f"       , lecture_part "
                             f"       , rate_posture "
                             f"       , rate_concentrate "
                             f"       , COUNT(*) "
                             f"       , AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"FROM     study_log "
                             f"WHERE    student_id = {session.get('user_id')} "
                             f"GROUP BY lecture_id "
                             f"       , lecture_part "
                             f"ORDER BY id ")
    data_dict = {}
    for row in data:
        if row[0] not in data_dict:
            data_dict[row[0]] = {}
        data_dict[row[0]][row[1]] = {
            'rate_posture': row[2],
            'rate_concentrate': row[3],
            'count': row[4],
            'avg_posture': row[5],
            'avg_concentrate': row[6]
        }
    print(data_dict)
    return render_template('student/total.html', data=data_dict)
