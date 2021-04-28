from arcafe import db


class User_02(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    create_date = db.Column(db.Date(), nullable=False)


class Usage_02(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    operationTime = db.Column(db.Float, nullable=False)
    longestOpenedTime = db.Column(db.Float, nullable=False)
    blinkCount = db.Column(db.Integer, nullable=False)
    warningCount = db.Column(db.Integer, nullable=False)
    alertCount = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.Date(), nullable=False)

