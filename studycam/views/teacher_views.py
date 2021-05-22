from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from studycam.models import User
from studycam import db
from studycam.models import StudyLog
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
    return redirect(url_for('teacher.total'))


@bp.route('/total/')
def total():
    data = db.engine.execute(f"SELECT   lecture_id "
                             f"       , lecture_part "
                             f"       , AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , COUNT(*) "
                             f"FROM     study_log "
                             f"WHERE    teacher_id = {session.get('user_id')} "
                             f"GROUP BY lecture_id "
                             f"       , lecture_part "
                             f"       , student_id "
                             f"ORDER BY id ")
    data_dict = {}
    rownum = 0
    for row in data:
        if row[0] not in data_dict:
            data_dict[row[0]] = {}
        data_dict[row[0]][row[1]] = {'rate_posture': row[2], 'rate_concentrate': row[3], 'count': row[4]}
        rownum += 1
    if rownum == 0:
        return render_template('teacher/empty.html')
    return render_template('teacher/total.html', data=data_dict)
