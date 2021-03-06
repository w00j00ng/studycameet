from flask import Blueprint, request, render_template, redirect, url_for
from flask import flash, session, g
from studycam.forms import UserCreateForm, UserLoginForm
from studycam.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from studycam import db
import datetime


bp = Blueprint('auth', __name__, url_prefix='/auth/')


@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            today_date = datetime.datetime.now().date()
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password1.data),
                email=form.email.data,
                div=form.div.data
            )
            db.session.add(user)
            db.session.commit()
            report_data = {
                "username": form.username.data,
                "email": form.email.data,
                "create_date": today_date
            }
            return render_template('auth/signup_finished.html', report_data=report_data)
        else:
            flash('이미 존재하는 사용자입니다.')
            return redirect(url_for('auth.signup'))
    return render_template('auth/signup.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
