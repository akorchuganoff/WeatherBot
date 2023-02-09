from config import State
from .models import User
from . import db, app


def get_current_state(user_id):
    with app.app_context():
        try:
            user = User.query.filter_by(chat_id=user_id).first()
            return user.state
        except Exception as ex:
            return State.S_START


def set_state(user_id, value):
    with app.app_context():
        try:
            user = User.query.filter_by(chat_id=user_id).first()
            user.state = value
            db.session.add(user)
            db.session.commit()
        except:
            user = User(
                chat_id=user_id,
                state=value,
                longitude=None,
                latitude=None
            )
            db.session.add(user)
            db.session.commit()

