from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Results(db.Model):
    __tablename__ = "compete_res"

    user_id = db.Column('user_id', db.INT, primary_key=True)
    status = db.Column('status', db.INT)
    user_ok = db.Column('user_ok', db.INT)
    model_ok = db.Column('model_ok', db.INT)
    uwins = db.Column('uwins', db.INT)
    uloses = db.Column('uloses', db.INT)
    uequals = db.Column('uequals', db.INT)