from flask import Blueprint, render_template, redirect, url_for
from mytools import detecter_cam
from threading import Thread
from studycam import db
from studycam.models import User, StudyLog
from flask import session, g
import datetime as dt


DEFAULT_LECTURE_ID = 1
DEFAULT_TEACHER_ID = 1
DEFAULT_STUDENT_ID = 2


bp = Blueprint('cambot', __name__, url_prefix='/cambot/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('cambot/index.html')


@bp.route('/execute/', methods=['POST'])
def execute():
    thread = Thread(target=detecter_cam.main())
    thread.start()
    thread.join()
    return redirect(url_for('cambot.index'))


@bp.route('/upload/', methods=["POST"])
def upload(report):
    print(report)
    lecture_id = DEFAULT_LECTURE_ID
    lecture_part = report['part_number']
    teacher_id = DEFAULT_TEACHER_ID
    student_id = DEFAULT_STUDENT_ID

    rate_posture, rate_concentrate = 0, 0
    rate_angry, rate_disgust, rate_fear, rate_happy, rate_sad = 0, 0, 0, 0, 0

    if g.user:
        student_id = session.get('user_id')
    rate_posture = (report['eye_data'][0] + report['eye_data'][1]) / report['loop_count']
    if (report['eye_data'][0] + report['eye_data'][1]) != 0:
        rate_concentrate = report['eye_data'][1] / (report['eye_data'][0] + report['eye_data'][1])

    if report['emotion_data']['Total'] != 0:
        rate_angry = report['emotion_data']['Angry'] / report['emotion_data']['Total']
        rate_disgust = report['emotion_data']['Disgust'] / report['emotion_data']['Total']
        rate_fear = report['emotion_data']['Fear'] / report['emotion_data']['Total']
        rate_happy = report['emotion_data']['Happy'] / report['emotion_data']['Total']
        rate_sad = report['emotion_data']['Sad'] / report['emotion_data']['Total']

    total_loop = report['loop_count']

    input_data = StudyLog(
        lecture_id=lecture_id,
        lecture_part=lecture_part,
        teacher_id=teacher_id,
        student_id=student_id,
        rate_posture=rate_posture,
        rate_concentrate=rate_concentrate,
        rate_angry=rate_angry,
        rate_disgust=rate_disgust,
        rate_fear=rate_fear,
        rate_happy=rate_happy,
        rate_sad=rate_sad,
        total_loop=total_loop,
        create_date=dt.datetime.today(),
        create_time=dt.datetime.now().hour
    )
    db.session.add(input_data)
    print("======================data added======================")

    return redirect(url_for('cambot.index'))


@bp.route('/commit_data/', methods=["POST"])
def commit_data():
    db.session.commit()
    print("======================data commited======================")
    return redirect(url_for('cambot.index'))
