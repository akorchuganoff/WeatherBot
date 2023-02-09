from . import db


class User(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer)
    longitude = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"User {self.chat_id}"
