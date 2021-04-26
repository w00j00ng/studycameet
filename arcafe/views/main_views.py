from flask import Blueprint, render_template
from arcafe.mytools import detect_blinks

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    detect_blinks.main()
    return render_template('main/index.html')
