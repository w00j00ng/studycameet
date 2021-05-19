from flask import Blueprint, render_template, redirect, url_for, request
from mytools import detecter_cam
from threading import Thread
from studycam import db
from studycam.models import User
from flask import session, g


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
def upload(report_data):
    user_id = session.get('user_id')
    print(report_data)
    # usage = Usage_02(username=request.form['username'],
    #                  operationTime=request.form['operationTime'],
    #                  totalWorkingTime=request.form['totalWorkingTime'],
    #                  longestOpenedTime=request.form['longestOpenedTime'],
    #                  blinkCount=request.form['blinkCount'],
    #                  warningCount=request.form['warningCount'],
    #                  alertCount=request.form['alertCount'],
    #                  create_date=today_date)
    # db.session.add(usage)
    return redirect(url_for('cambot.index'))


@bp.route('/commit_data/', methods=["POST"])
def commit_data():
    db.session.commit()
    return redirect(url_for('cambot.index'))
