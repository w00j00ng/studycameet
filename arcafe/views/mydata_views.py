from flask import Blueprint, render_template
from flask import session, g
from arcafe.models import User_02
from arcafe import db
import pandas as pd


bp = Blueprint('mydata', __name__, url_prefix='/mydata/')


mydataList = []


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User_02.query.get(user_id)


@bp.route('/')
def mydata():
    global mydataList
    query_mydata = db.engine.execute(f'SELECT * FROM usage_02 WHERE username = "{g.user.username}" ORDER BY id')
    all_rows = [row for row in query_mydata]
    print(all_rows)
    return render_template('mydata/index.html', result=all_rows)


@bp.route('/bydate/')
def bydate():
    global mydataList
    query_mydata = db.engine.execute(f"SELECT 'id'"
                                     f"     , 'username'"
                                     f'     , SUM(operationTime)'
                                     f'     , SUM(totalWorkingTime)'
                                     f'     , SUM(totalWorkingTime) / SUM(operationTime) * 100'
                                     f'     , SUM(blinkCount)'
                                     f'     , SUM(warningCount)'
                                     f'     , SUM(alertCount)'
                                     f'     , create_date '
                                     f'FROM usage_02 '
                                     f'WHERE username = "{g.user.username}" '
                                     f'GROUP BY create_date')
    all_rows = [row for row in query_mydata]
    print(all_rows)
    return render_template('mydata/bydate.html', result=all_rows)


@bp.route('/detail/')
def detail():
    global mydataList
    mydataDf = pd.DataFrame(mydataList,
                            columns=[
                                'id',
                                'username',
                                'operationTime',
                                'totalWorkingTime',
                                'longestOpenedTime',
                                'blinkCount',
                                'warningCount',
                                'alertCount',
                                'create_date'
                            ])
    mydataDf.drop(['id', 'username'], inplace=True)
    return render_template('mydata/detail.html', data=mydataList, mydataDf=mydataDf)
