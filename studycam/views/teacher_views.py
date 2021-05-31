from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from studycam.models import User
from studycam import db
import heapq


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
    return redirect(url_for('teacher.by_lecture'))


@bp.route('/by_lecture/')
def by_lecture():
    data = db.engine.execute(
        f"SELECT   lecture_id "
        f"       , lecture_part "
        f"       , AVG(posture) "
        f"       , AVG(concentrate) "
        f"       , AVG(angry) "
        f"       , AVG(disgust) "
        f"       , AVG(fear) "
        f"       , AVG(happy) "
        f"       , AVG(sad) "
        f"       , COUNT (distinct student_id) "
        f"FROM ( "
        f"         SELECT   student_id "
        f"                , lecture_id "
        f"                , lecture_part "
        f"                , AVG(rate_posture)     posture "
        f"                , AVG(rate_concentrate) concentrate "
        f"                , AVG(rate_angry)       angry "
        f"                , AVG(rate_disgust)     disgust "
        f"                , AVG(rate_fear)        fear "
        f"                , AVG(rate_happy)       happy "
        f"                , AVG(rate_sad)         sad "
        f"         FROM     study_log "
        f"         WHERE    teacher_id = {session.get('user_id')} "
        f"         GROUP BY student_id "
        f"                , lecture_id "
        f"                , lecture_part "
        f"     ) "
        f"GROUP BY lecture_id "
        f"       , lecture_part"
    )
    report = {}
    row_num = 0
    for row in data:
        if row[0] not in report:
            report[row[0]] = {}
        emotion_list = [row[4], row[5], row[6], row[7], row[8]]
        emotion_label = ['스트레스', '우울', '불안', '행복', '슬픔']
        emotion_rank = heapq.nlargest(2, range(len(emotion_list)), key=emotion_list.__getitem__)
        report[row[0]][row[1]] = {
            'rate_posture': row[2],
            'grade_posture': get_grade(row[2]),
            'rate_concentrate': row[3],
            'grade_concentrate': get_grade(row[3]),
            'max_emotion': emotion_label[emotion_rank[0]],
            'max_emotion_rate': emotion_list[emotion_rank[0]],
            'second_emotion': emotion_label[emotion_rank[1]],
            'second_emotion_rate': emotion_list[emotion_rank[1]],
            'student_count': row[9],
        }
        row_num += 1
    if row_num == 0:
        return render_template('teacher/empty.html')
    return render_template('teacher/by_lecture.html', report=report)


def get_grade(rate):
    if rate > 0.9:
        grade = "아주좋음"
    elif rate > 0.6:
        grade = "좋음"
    elif rate > 0.4:
        grade = "보통"
    elif rate > 0.2:
        grade = "나쁨"
    else:
        grade = "아주나쁨"
    return grade
