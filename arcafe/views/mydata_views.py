from flask import Blueprint, render_template, redirect, url_for
from flask import session, g
from arcafe.models import User_02
from arcafe import db
import pandas as pd


bp = Blueprint('mydata', __name__, url_prefix='/mydata/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User_02.query.get(user_id)


@bp.route('/')
def mydata():
    return redirect(url_for('mydata.bydate'))


@bp.route('/bydate/')
def bydate():
    query_mydata = db.engine.execute(f"SELECT SUM(operationTime) / 60"
                                     f'     , SUM(totalWorkingTime) / 60'
                                     f'     , SUM(totalWorkingTime) / SUM(operationTime) * 100'
                                     f'     , SUM(blinkCount) / SUM(totalWorkingTime) * 60'
                                     f'     , SUM(warningCount)/ SUM(totalWorkingTime) * 60'
                                     f'     , SUM(alertCount)/ SUM(totalWorkingTime) * 60'
                                     f'     , create_date '
                                     f'FROM usage_02 '
                                     f'WHERE username = "{g.user.username}" '
                                     f'GROUP BY create_date '
                                     f'ORDER BY create_date desc')
    all_rows = [row for row in query_mydata]
    return render_template('mydata/bydate.html', result=all_rows)


@bp.route('/byweek/')
def byweek():
    query_mydata = db.engine.execute(f"SELECT SUM(operationTime) / 60"
                                     f'     , SUM(totalWorkingTime) / 60'
                                     f"     , SUM(totalWorkingTime) / SUM(operationTime) * 100"
                                     f'     , SUM(blinkCount) / SUM(totalWorkingTime) * 60'
                                     f'     , SUM(warningCount)/ SUM(totalWorkingTime) * 60'
                                     f'     , SUM(alertCount)/ SUM(totalWorkingTime) * 60'
                                     f'     , WEEKDAY(create_date) '
                                     f'FROM usage_02 '
                                     f'WHERE username = "{g.user.username}" '
                                     f'GROUP BY WEEKDAY(create_date) '
                                     f'ORDER BY WEEKDAY(create_date)')
    weekname = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

    all_rows = [row for row in query_mydata]

    return render_template('mydata/byweek.html', result=all_rows, weekname=weekname)


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
