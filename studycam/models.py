from studycam import db


class User_02(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    div = db.Column(db.String(1), nullable=False)


class Lecture_02(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    subject_number = db.Column(db.Integer, nullable=True)


class StudentLog_02(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    lecture_id = db.Column(db.Integer, nullable=False)
    phone_count = db.Column(db.Integer, nullable=True)
    emotion = db.Column(db.String(150), nullable=True)
    operation_time = db.Column(db.Float, nullable=True)
    study_time = db.Column(db.Float, nullable=True)


class TeacherLog_02(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    lecture_id = db.Column(db.Integer, nullable=False)
    lecture_part = db.Column(db.Integer, nullable=True)
    phone_issue = db.Column(db.Integer, nullable=True)
    concentrate_issue = db.Column(db.Float, nullable=True)
