from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from studycam.models import User
from studycam import db


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
    return redirect(url_for('student.by_lecture'))


@bp.route('/by_lecture/')
def by_lecture():
    data = db.engine.execute(
        f"SELECT   lecture_id "
        f"       , lecture_part "
        f"       , AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , COUNT(*) "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY lecture_id "
        f"       , lecture_part "
        f"ORDER BY id "
    )

    report = {}
    row_num, posture_sum, concentrate_sum = 0, 0, 0
    for row in data:
        if row[0] not in report:
            report[row[0]] = {}
        report[row[0]][row[1]] = {
            'rate_concentrate': row[2],
            'grade_concentrate': get_grade(row[2]),
            'rate_posture': row[3],
            'grade_posture': get_grade(row[3]),
            'count': row[4]
        }
        posture_sum += row[2]
        concentrate_sum += row[3]
        row_num += 1
    if row_num == 0:
        return render_template('student/empty.html')
    avg_info = [
        get_grade(posture_sum / row_num),
        posture_sum / row_num,
        get_grade(concentrate_sum / row_num),
        concentrate_sum / row_num
    ]
    return render_template('student/by_lecture.html', report=report, avg_info=avg_info)


@bp.route('/by_date/')
def by_date():
    data = db.engine.execute(
        f"SELECT   AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , create_date "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY create_date "
        f"ORDER BY create_date "
    )
    result = []
    for row in data:
        result.append({
            'grade_concentrate': get_grade(row[0]),
            'rate_concentrate': row[0],
            'grade_posture': get_grade(row[1]),
            'rate_posture': row[1],
            'create_date': row[2]
        })
    return render_template('student/by_date.html', result=result)


@bp.route('/by_week/')
def by_week():
    data = db.engine.execute(
        f"SELECT   AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , strftime('%w', create_date) "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY strftime('%w', create_date) "
        f"ORDER BY strftime('%w', create_date) "
    )
    week_name = {"0": "일요일", "1": "월요일", "2": "화요일", "3": "수요일", "4": "목요일", "5": "금요일", "6": "토요일"}
    report = []
    for row in data:
        report.append({
            'grade_concentrate': get_grade(row[0]),
            'rate_concentrate': row[0],
            'grade_posture': get_grade(row[1]),
            'rate_posture': row[1],
            'weekday': week_name[row[2]]
        })
    return render_template('student/by_week.html', report=report)


@bp.route('/by_time/')
def by_time():
    data = db.engine.execute(
        f"SELECT   AVG(rate_concentrate) "
        f"       , AVG(rate_posture) "
        f"       , create_time "
        f"FROM     study_log "
        f"WHERE    student_id = {session.get('user_id')} "
        f"GROUP BY create_time "
        f"ORDER BY create_time "
    )
    report = []
    for row in data:
        report.append({
            'grade_concentrate': get_grade(row[0]),
            'rate_concentrate': row[0],
            'grade_posture': get_grade(row[1]),
            'rate_posture': row[1],
            'create_time': row[2]
        })
    return render_template('student/by_time.html', report=report)


def get_grade(rate):
    if rate > 0.9:
        grade = "아주좋음"
    elif rate > 0.6:
        grade = "좋음"
    elif rate > 0.3:
        grade = "보통"
    elif rate > 0.1:
        grade = "나쁨"
    else:
        grade = "아주나쁨"
    return grade
