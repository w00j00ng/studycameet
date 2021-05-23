from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from studycam.models import User
from studycam import db
from studycam.models import StudyLog
from sqlalchemy import and_
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
    return redirect(url_for('teacher.total'))


@bp.route('/total/')
def total():
    data = db.engine.execute(f"SELECT   lecture_id "
                             f"       , lecture_part "
                             f"       , AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , AVG(rate_angry) "
                             f"       , AVG(rate_disgust) "
                             f"       , AVG(rate_fear) "
                             f"       , AVG(rate_happy) "
                             f"       , AVG(rate_sad) "
                             f"       , COUNT(*) "
                             f"FROM     study_log "
                             f"WHERE    teacher_id = {session.get('user_id')} "
                             f"GROUP BY lecture_id "
                             f"       , lecture_part "
                             f"ORDER BY id ")
    data_dict = {}
    rownum = 0
    for row in data:
        if row[0] not in data_dict:
            data_dict[row[0]] = {}
        emotion_list = [row[4], row[5], row[6], row[7], row[8]]
        emotion_label = ['스트레스', '우울', '불안', '행복', '슬픔']
        emotion_rank = heapq.nlargest(2, range(len(emotion_list)), key=emotion_list.__getitem__)
        data_dict[row[0]][row[1]] = {
            'rate_posture': row[2],
            'rate_concentrate': row[3],
            'max_emotion': emotion_label[emotion_rank[0]],
            'max_emotion_rate': emotion_list[emotion_rank[0]],
            'second_emotion': emotion_label[emotion_rank[1]],
            'second_emotion_rate': emotion_list[emotion_rank[1]],
            'count': row[9]
        }
        rownum += 1
    if rownum == 0:
        return render_template('teacher/empty.html')
    return render_template('teacher/total.html', data=data_dict)
