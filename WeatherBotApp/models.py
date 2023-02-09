from . import db


class City(db.Model):
    # __tablename__ = "cities"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    longitude = db.Column(db.Float())
    latitude = db.Column(db.Float())
    users = db.relationship('User', backref='city', cascade='all,delete-orphan')


class User(db.Model):
    # __tablename__ = "users"
    chat_id = db.Column(db.Integer(), primary_key=True)
    state = db.Column(db.Integer())
    city_id = db.Column(db.Integer(), db.ForeignKey(City.id))

    def __repr__(self):
        return f"User {self.chat_id}"