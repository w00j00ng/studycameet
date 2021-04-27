from flask import Blueprint, render_template, redirect, url_for
from arcafe.mytools import detect_blinks
from threading import Thread
import time


bp = Blueprint('nagbot', __name__, url_prefix='/nagbot/')

startTime = 0
prevBlinkTime = 0
lastBlinkTime = 0
longestOpenedTime = 0
blinkCount = 0


@bp.route('/')
def index():
    global startTime, blinkCount, longestOpenedTime
    operationTime = time.time() - startTime
    return render_template('nagbot/index.html',
                           operationTime=operationTime,
                           longestOpenedTime = longestOpenedTime,
                           blinkCount=blinkCount)


@bp.route('/execute/', methods=['POST'])
def execute():
    global startTime, prevBlinkTime, lastBlinkTime, longestOpenedTime
    startTime = time.time()
    prevBlinkTime = time.time()
    lastBlinkTime = time.time()
    longestOpenedTime = 0
    thread = Thread(target=detect_blinks.main())
    thread.start()
    thread.join()
    return redirect(url_for('nagbot.index'))


@bp.route('/blink/', methods=["POST"])
def blink():
    global blinkCount, prevBlinkTime, lastBlinkTime, longestOpenedTime
    print("Blink")
    if blinkCount == 0:
        prevBlinkTime = time.time()
    lastBlinkTime = time.time()
    blinkCount += 1
    if lastBlinkTime - prevBlinkTime > longestOpenedTime:
        longestOpenedTime = lastBlinkTime - prevBlinkTime
    prevBlinkTime = time.time()
    return redirect(url_for('nagbot.index'))


@bp.route('/warning/', methods=["POST"])
def warning():
    global blinkCount, lastBlinkTime
    print("Warning")
    return redirect(url_for('nagbot.index'))


@bp.route('/alert/', methods=["POST"])
def alert():
    global blinkCount, lastBlinkTime
    print("Alert")
    return redirect(url_for('nagbot.index'))


@bp.route('/noface/', methods=["POST"])
def noface():
    global blinkCount, lastBlinkTime
    print("No Face Detected")
    return redirect(url_for('nagbot.index'))
