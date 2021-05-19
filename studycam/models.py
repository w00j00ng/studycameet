from studycam import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    div = db.Column(db.String(1), nullable=False)


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    subject_number = db.Column(db.Integer, nullable=True)


class StudyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lecture_id = db.Column(db.Integer, nullable=True)
    lecture_part = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, nullable=True)
    student_id = db.Column(db.Integer, nullable=False)
    rate_posture = db.Column(db.Integer, nullable=False)
    rate_concentrate = db.Column(db.Integer, nullable=False)
    rate_angry = db.Column(db.Integer, nullable=False)
    rate_disgust = db.Column(db.Integer, nullable=False)
    rate_happy = db.Column(db.Integer, nullable=False)
    rate_sad = db.Column(db.Integer, nullable=False)
