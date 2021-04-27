from flask import Blueprint, render_template, redirect, url_for
from mytools import detect_blinks
from threading import Thread
import time


bp = Blueprint('nagbot', __name__, url_prefix='/nagbot/')

startTime, prevBlinkTime, lastBlinkTime, longestOpenedTime = 0, 0, 0, 0
blinkCount, warningCount, alertCount = 0, 0, 0


@bp.route('/')
def index():
    global startTime, longestOpenedTime
    global blinkCount, warningCount, alertCount

    if longestOpenedTime == 0:
        return render_template('nagbot/index.html')

    operationTime = time.time() - startTime
    return render_template('nagbot/result.html',
                           operationTime=operationTime, longestOpenedTime=longestOpenedTime,
                           blinkCount=blinkCount, warningCount=warningCount, alertCount=alertCount)


@bp.route('/execute/', methods=['POST'])
def execute():
    global startTime, prevBlinkTime, lastBlinkTime, longestOpenedTime
    global blinkCount, warningCount, alertCount
    startTime = time.time()
    prevBlinkTime, lastBlinkTime = startTime, startTime
    longestOpenedTime = 0
    blinkCount, warningCount, alertCount = 0, 0, 0
    thread = Thread(target=detect_blinks.main())
    thread.start()
    thread.join()
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
    global blinkCount, lastBlinkTime
    alertCount += 1
    print("Alert")
    return redirect(url_for('nagbot.index'))


@bp.route('/noface/', methods=["POST"])
def noface():
    global blinkCount, lastBlinkTime
    print("No Face Detected")
    return redirect(url_for('nagbot.index'))
