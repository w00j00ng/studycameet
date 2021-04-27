from flask import Blueprint, render_template, redirect, url_for
from arcafe.mytools import detect_blinks
from threading import Thread

bp = Blueprint('nagbot', __name__, url_prefix='/nagbot/')


@bp.route('/')
def index():
    return render_template('nagbot/index.html')


@bp.route('/execute/', methods=['POST'])
def execute():
    thread = Thread(target=detect_blinks.main())
    thread.start()
    thread.join()
    return redirect(url_for('nagbot.index'))


@bp.route('/blink/', methods=["POST"])
def blink():
    print("Blink")
    return redirect(url_for('nagbot.index'))


@bp.route('/warning/', methods=["POST"])
def warning():
    print("Warning")
    return redirect(url_for('nagbot.index'))


@bp.route('/alert/', methods=["POST"])
def alert():
    print("Alert")
    return redirect(url_for('nagbot.index'))


@bp.route('/noface/', methods=["POST"])
def noface():
    print("No Face Detected")
    return redirect(url_for('nagbot.index'))
