from flask import Blueprint, render_template, redirect, url_for
from arcafe.mytools import detect_blinks
from threading import Thread

bp = Blueprint('nagbot', __name__, url_prefix='/nagbot/')


@bp.route('/index/')
def index():
    return render_template('nagbot/index.html')


@bp.route('/execute/', methods=['POST'])
def execute():
    thread = Thread(target=detect_blinks.main())
    thread.start()
    return redirect(url_for('nagbot.index'))
