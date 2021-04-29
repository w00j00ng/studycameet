from flask import Blueprint, render_template, redirect, url_for, g, request
from mytools import detect_blinks
from threading import Thread
import time
import datetime
from arcafe import db
from arcafe.models import Usage_02
from flask import session, g
from arcafe.models import User_02


bp = Blueprint('nagbot', __name__, url_prefix='/nagbot/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User_02.query.get(user_id)

startTime, endTime, prevBlinkTime, lastBlinkTime, longestOpenedTime = 0, 0, 0, 0, 0
totalRestTime, restStartTime = 0, 0
blinkCount, warningCount, alertCount = 0, 0, 0
bRestCheck = False


@bp.route('/')
def index():
    global startTime, endTime, longestOpenedTime
    global blinkCount, warningCount, alertCount

    if longestOpenedTime == 0:
        return render_template('nagbot/index.html')

    operationTime = endTime - startTime
    today_date = datetime.datetime.now().date()

    danger, lazy=False, False
    if totalRestTime / operationTime < 0.05:
        danger=True
    elif totalRestTime / operationTime > 0.2:
        lazy=True

    return render_template('nagbot/result.html',
                           operationTime=operationTime,
                           longestOpenedTime=longestOpenedTime,
                           totalWorkingTime=operationTime-totalRestTime,
                           blinkCount=blinkCount,
                           warningCount=warningCount,
                           alertCount=alertCount,
                           today_date=today_date,
                           danger=danger,
                           lazy=lazy)


@bp.route('/execute/', methods=['POST'])
def execute():
    global startTime, endTime, prevBlinkTime, lastBlinkTime, longestOpenedTime
    global blinkCount, warningCount, alertCount
    startTime = time.time()
    prevBlinkTime, lastBlinkTime = startTime, startTime
    longestOpenedTime = 0
    blinkCount, warningCount, alertCount = 0, 0, 0
    thread = Thread(target=detect_blinks.main())
    thread.start()
    thread.join()
    endTime = time.time()
    return redirect(url_for('nagbot.index'))


@bp.route('/upload/', methods=["POST"])
def upload():
    today_date = datetime.datetime.now().date()
    usage = Usage_02(username=request.form['username'],
                     operationTime=request.form['operationTime'],
                     totalWorkingTime=request.form['totalWorkingTime'],
                     longestOpenedTime=request.form['longestOpenedTime'],
                     blinkCount=request.form['blinkCount'],
                     warningCount=request.form['warningCount'],
                     alertCount=request.form['alertCount'],
                     create_date=today_date)
    db.session.add(usage)
    db.session.commit()

    return redirect(url_for('nagbot.index'))


@bp.route('/blink/', methods=["POST"])
def blink():
    global blinkCount, prevBlinkTime, lastBlinkTime, longestOpenedTime
    lastBlinkTime = time.time()
    print("Blink")
    if blinkCount == 0:
        prevBlinkTime = lastBlinkTime
        longestOpenedTime = lastBlinkTime - startTime
    else:
        prevBlinkTime = lastBlinkTime
    blinkCount += 1
    if lastBlinkTime - prevBlinkTime > longestOpenedTime:
        longestOpenedTime = lastBlinkTime - prevBlinkTime
    return redirect(url_for('nagbot.index'))


@bp.route('/warning/', methods=["POST"])
def warning():
    global warningCount
    warningCount += 1
    print("Warning")
    return redirect(url_for('nagbot.index'))


@bp.route('/alert/', methods=["POST"])
def alert():
    global blinkCount, lastBlinkTime, alertCount
    alertCount += 1
    print("Alert")
    return redirect(url_for('nagbot.index'))


@bp.route('/noface/', methods=["POST"])
def noface():
    global blinkCount, lastBlinkTime
    print("No Face Detected")
    return redirect(url_for('nagbot.index'))


@bp.route('/working/', methods=["POST"])
def working():
    global bRestCheck, restStartTime, totalRestTime
    if bRestCheck:
        totalRestTime += time.time() - restStartTime
        bRestCheck = False
    return redirect(url_for('nagbot.index'))


@bp.route('/rest/', methods=["POST"])
def rest():
    global bRestCheck, restStartTime
    if not bRestCheck:
        print("Rest")
        restStartTime = time.time()
        bRestCheck = True
    return redirect(url_for('nagbot.index'))
