from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from studycam.models import User
from studycam import db
from studycam.models import StudyLog
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
    return redirect(url_for('student.bylecture'))


@bp.route('/bylecture/')
def bylecture():
    data = db.engine.execute(f"SELECT   lecture_id "
                             f"       , lecture_part "
                             f"       , AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , COUNT(*) "
                             f"FROM     study_log "
                             f"WHERE    student_id = {session.get('user_id')} "
                             f"GROUP BY lecture_id "
                             f"       , lecture_part "
                             f"ORDER BY id ")

    data_dict = {}
    rownum, posture_sum, concentrate_sum = 0, 0, 0
    for row in data:
        if row[0] not in data_dict:
            data_dict[row[0]] = {}
        data_dict[row[0]][row[1]] = {'rate_posture': row[2], 'rate_concentrate': row[3], 'count': row[4]}
        posture_sum += row[2]
        concentrate_sum += row[3]
        rownum += 1
    if rownum == 0:
        return render_template('student/empty.html')
    avginfo = [posture_sum / rownum, concentrate_sum / rownum]
    return render_template('student/bylecture.html', data=data_dict, avginfo=avginfo, rownum=rownum)


@bp.route('/bydate/')
def bydate():
    data = db.engine.execute(f"SELECT   AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , create_date "
                             f"FROM     study_log "
                             f"WHERE    student_id = {session.get('user_id')} "
                             f"GROUP BY create_date "
                             f"ORDER BY create_date ")
    all_rows = [row for row in data]
    return render_template('student/bydate.html', result=all_rows)


@bp.route('/byweek/')
def byweek():
    data = db.engine.execute(f"SELECT   AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , strftime('%w', create_date) "
                             f"FROM     study_log "
                             f"WHERE    student_id = {session.get('user_id')} "
                             f"GROUP BY strftime('%w', create_date) "
                             f"ORDER BY strftime('%w', create_date) ")
    all_rows = [row for row in data]
    weekname = {"0": "월요일", "1": "화요일", "2": "수요일", "3": "목요일", "4": "금요일", "5": "토요일", "6": "일요일"}
    return render_template('student/byweek.html', result=all_rows, weekname=weekname)


@bp.route('/bytime/')
def bytime():
    data = db.engine.execute(f"SELECT   AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , create_time "
                             f"FROM     study_log "
                             f"WHERE    student_id = {session.get('user_id')} "
                             f"GROUP BY create_time "
                             f"ORDER BY create_time ")
    all_rows = [row for row in data]
    return render_template('student/bytime.html', result=all_rows)
