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
    return redirect(url_for('teacher.bylecture'))


@bp.route('/bylecture/')
def bylecture():
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
    return render_template('teacher/bylecture.html', data=data_dict)


@bp.route('/bydate/')
def bydate():
    data = db.engine.execute(f"SELECT   create_date "
                             f"       , AVG(rate_concentrate) "
                             f"       , AVG(rate_posture) "
                             f"       , AVG(rate_angry) "
                             f"       , AVG(rate_disgust) "
                             f"       , AVG(rate_fear) "
                             f"       , AVG(rate_happy) "
                             f"       , AVG(rate_sad) "
                             f"       , COUNT(*) "
                             f"FROM     study_log "
                             f"WHERE    teacher_id = {session.get('user_id')} "
                             f"GROUP BY create_date "
                             f"ORDER BY create_date ")
    report_data = []
    for row in data:
        emotion_list = [row[3], row[4], row[5], row[6], row[7]]
        emotion_label = ['스트레스', '우울', '불안', '행복', '슬픔']
        emotion_rank = heapq.nlargest(2, range(len(emotion_list)), key=emotion_list.__getitem__)
        report_data.append([
            row[0], row[1], row[2],
            emotion_label[emotion_rank[0]],
            emotion_list[emotion_rank[0]],
            emotion_label[emotion_rank[1]],
            emotion_list[emotion_rank[1]],
            row[8]
        ])
    print(report_data)
    return render_template('teacher/bydate.html', report_data=report_data)


@bp.route('/byweek/')
def byweek():
    data = db.engine.execute(f"SELECT   AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , AVG(rate_angry) "
                             f"       , AVG(rate_disgust) "
                             f"       , AVG(rate_fear) "
                             f"       , AVG(rate_happy) "
                             f"       , AVG(rate_sad) "
                             f"       , strftime('%w', create_date) "
                             f"       , COUNT(*) "
                             f"FROM     study_log "
                             f"WHERE    teacher_id = {session.get('user_id')} "
                             f"GROUP BY strftime('%w', create_date) "
                             f"ORDER BY strftime('%w', create_date) ")
    all_rows = [row for row in data]
    report_data = []
    for row in all_rows:
        emotion_list = [row[2], row[3], row[4], row[5], row[6]]
        emotion_label = ['스트레스', '우울', '불안', '행복', '슬픔']
        emotion_rank = heapq.nlargest(2, range(len(emotion_list)), key=emotion_list.__getitem__)
        report_data.append([
            row[0], row[1],
            emotion_label[emotion_rank[0]],
            emotion_list[emotion_rank[0]],
            emotion_label[emotion_rank[1]],
            emotion_list[emotion_rank[1]],
            0,
            row[7],
            row[8]
        ])
    weekname = {"0": "월요일", "1": "화요일", "2": "수요일", "3": "목요일", "4": "금요일", "5": "토요일", "6": "일요일"}
    return render_template('teacher/byweek.html', report_data=report_data, weekname=weekname)


@bp.route('/bytime/')
def bytime():
    data = db.engine.execute(f"SELECT   AVG(rate_posture) "
                             f"       , AVG(rate_concentrate) "
                             f"       , AVG(rate_angry) "
                             f"       , AVG(rate_disgust) "
                             f"       , AVG(rate_fear) "
                             f"       , AVG(rate_happy) "
                             f"       , AVG(rate_sad) "
                             f"       , create_time "
                             f"       , COUNT(*) "
                             f"FROM     study_log "
                             f"WHERE    teacher_id = {session.get('user_id')} "
                             f"GROUP BY create_time "
                             f"ORDER BY create_time ")
    all_rows = [row for row in data]
    report_data = []
    for row in all_rows:
        emotion_list = [row[2], row[3], row[4], row[5], row[6]]
        emotion_label = ['스트레스', '우울', '불안', '행복', '슬픔']
        emotion_rank = heapq.nlargest(2, range(len(emotion_list)), key=emotion_list.__getitem__)
        report_data.append([
            row[0], row[1],
            emotion_label[emotion_rank[0]],
            emotion_list[emotion_rank[0]],
            emotion_label[emotion_rank[1]],
            emotion_list[emotion_rank[1]],
            0,
            row[7],
            row[8]
        ])
    return render_template('teacher/bytime.html', result=report_data)
