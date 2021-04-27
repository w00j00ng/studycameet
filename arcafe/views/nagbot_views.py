from flask import Blueprint, render_template, Response
from arcafe.mytools import detect_blinks

bp = Blueprint('nagbot', __name__, url_prefix='/nagbot/')


@bp.route('/index/')
def index():
    return render_template('nagbot/index.html')


@bp.route('/execute/')
def execute():
    return Response(detect_blinks.main())
